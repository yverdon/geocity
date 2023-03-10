import io
from collections import defaultdict
from datetime import datetime, timedelta
from itertools import groupby

from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput
from captcha.fields import CaptchaField
from constance import config
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Fieldset, Layout
from django import forms
from django.conf import settings
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis import forms as geoforms
from django.core.exceptions import ValidationError
from django.core.files import File
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import transaction
from django.db.models import Max, Q
from django.forms import modelformset_factory
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from geocity.apps.accounts.models import (
    PUBLIC_TYPE_CHOICES,
    AdministrativeEntity,
    PermitDepartment,
)
from geocity.fields import AddressWidget, AdvancedGeometryWidget

from ..forms.models import Price
from ..reports.services import generate_report_pdf_as_response
from . import models, permissions, services
from .payments.models import SubmissionPrice

input_type_mapping = {
    models.Field.INPUT_TYPE_TEXT: forms.CharField,
    models.Field.INPUT_TYPE_CHECKBOX: forms.BooleanField,
    models.Field.INPUT_TYPE_NUMBER: forms.FloatField,
    models.Field.INPUT_TYPE_FILE: forms.FileField,
    models.Field.INPUT_TYPE_ADDRESS: forms.CharField,
    models.Field.INPUT_TYPE_DATE: forms.DateField,
    models.Field.INPUT_TYPE_LIST_SINGLE: forms.ChoiceField,
    models.Field.INPUT_TYPE_LIST_MULTIPLE: forms.MultipleChoiceField,
    models.Field.INPUT_TYPE_REGEX: forms.CharField,
}


def _title_html_representation(prop, for_summary=False):
    base = f"<h5 class='propertyTitle'>{prop.name}</h5>"
    if not for_summary and prop.help_text:
        base = f"{base}<small>{prop.help_text}</small>"
    return base


def _file_download_html_representation(prop, for_summary=False):
    if not for_summary and prop.file_download:
        description = prop.help_text if prop.help_text else _("Télécharger le fichier")
        return f"""<strong>{prop.name}:</strong>
            <i class="fa fa-download" aria-hidden="true"></i>
            <a class="file_download" href="{reverse('submissions:field_file_download', kwargs={'path': prop.file_download})}" target="_blank" rel="noreferrer">{description}</a>"""
    return ""


non_value_input_type_mapping = {
    models.Field.INPUT_TYPE_TITLE: _title_html_representation,
    models.Field.INPUT_TYPE_FILE_DOWNLOAD: _file_download_html_representation,
}


def get_field_cls_for_field(field):
    try:
        return input_type_mapping[field.input_type]
    except KeyError as e:
        raise KeyError(f"Field of type {e} is not supported.")


def regroup_by_ofs_id(entities):
    return groupby(entities.order_by("ofs_id"), lambda entity: entity.ofs_id)


def disable_form(form, editable_fields=None):
    for field in form.fields.values():
        if editable_fields and field.label in editable_fields:
            continue
        field.disabled = True

    if not editable_fields:
        form.disabled = True


class DisabledChoicesMixin:
    @property
    def disabled_choices(self):
        return getattr(self, "_disabled_choices", [])

    @disabled_choices.setter
    def disabled_choices(self, other):
        self._disabled_choices = other

    def create_option(
        self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option = super().create_option(
            name, value, label, selected, index, subindex, attrs
        )
        if value in self.disabled_choices:
            option["attrs"]["disabled"] = "disabled"
        return option


class GroupedRadioWidget(forms.RadioSelect):
    template_name = "submissions/widgets/groupedradio.html"

    class Media:
        css = {"all": ("customWidgets/GroupedRadio/groupedradio.css",)}


class CheckboxSelectMultipleWidget(DisabledChoicesMixin, forms.CheckboxSelectMultiple):
    template_name = "submissions/widgets/multipleselect.html"
    option_template_name = "submissions/widgets/checkbox_option.html"


class SingleFormRadioSelectWidget(DisabledChoicesMixin, forms.RadioSelect):
    template_name = "submissions/widgets/categorized_groupedradio.html"


class AdministrativeEntityForm(forms.Form):
    administrative_entity = forms.ModelChoiceField(
        label=_("Entité administrative"),
        widget=GroupedRadioWidget(),
        queryset=AdministrativeEntity.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        self.user = kwargs.pop("user", None)
        administrative_entities = kwargs.pop("administrative_entities")

        if self.instance:
            initial = {
                **kwargs.get("initial", {}),
                "administrative_entity": self.instance.administrative_entity.pk,
            }
        else:
            initial = {}

        kwargs["initial"] = initial

        super().__init__(*args, **kwargs)

        self.fields["administrative_entity"].choices = [
            (ofs_id, [(entity.pk, entity.name) for entity in entities])
            for ofs_id, entities in regroup_by_ofs_id(administrative_entities)
        ]

    def save(self, author):
        administrative_entity_instance = AdministrativeEntity.objects.get(
            pk=self.cleaned_data["administrative_entity"].pk
        )

        if not self.instance:
            return models.Submission.objects.create(
                administrative_entity=administrative_entity_instance,
                author=author,
            )
        else:
            self.instance.set_administrative_entity(administrative_entity_instance)
            return self.instance


class FormChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.name


class FormsSelectForm(forms.Form):
    prefix = "forms"
    selected_forms = forms.MultipleChoiceField(widget=CheckboxSelectMultipleWidget())

    def __init__(self, instance, form_categories=None, *args, **kwargs):
        self.instance = instance
        self.user = kwargs.pop("user", None)
        form_categories = form_categories or []
        selected_forms = list(
            self.instance.selected_forms.values_list("form_id", flat=True)
        )

        initial = {"selected_forms": selected_forms}

        super().__init__(*args, **{**kwargs, "initial": initial})
        user_can_view_private_form = self.user.has_perm("submissions.view_private_form")

        forms_filter = Q()

        if form_categories:
            forms_filter &= Q(category__in=form_categories)

        integrator_admin = self.user.groups.filter(
            permit_department__is_integrator_admin=True
        ).first()

        user_administrative_entities = AdministrativeEntity.objects.associated_to_user(
            self.user
        )

        if not self.user.is_superuser:
            if integrator_admin:
                """An integrator can fill all forms he owns + public ones"""
                forms_filter &= Q(integrator=integrator_admin) | Q(is_public=True)
            elif user_administrative_entities and user_can_view_private_form:
                """User is trusted and associated to administrative entities,
                he can fill private forms for those administrative entities
                if granted permission 'view_private_form'"""
                forms_filter &= Q(
                    administrative_entities__in=user_administrative_entities
                ) | Q(is_public=True)
            elif not user_can_view_private_form or not user_administrative_entities:
                """Untrusted users or user not granted with view_private_form can only fill public forms"""
                forms_filter &= Q(is_public=True)

        forms = (
            models.Form.objects.filter(
                Q(
                    forms_filter,
                    administrative_entities=self.instance.administrative_entity,
                    is_anonymous=self.user.userprofile.is_temporary,
                )
                | Q(pk__in=selected_forms)
            )
            .distinct()
            .select_related("category")
            .order_by("order")
        )

        forms_by_category_dict = {}
        for form in forms:
            forms_by_category_dict.setdefault(form.category, []).append(form)

        forms_by_category = []
        disabled_choices = set()
        for category, forms in sorted(
            forms_by_category_dict.items(), key=lambda item: slugify(item[0].name)
        ):
            forms_list = []
            for form in forms:
                form_name = form.name
                if form.has_exceeded_maximum_submissions():
                    form_name = f"{form_name} <span class='px-5 text-danger'>{form.max_submissions_message}</span>"
                    disabled_choices.add(form.pk)
                forms_list.append((form.pk, form_name))

            forms_by_category.append((category, forms_list))

        self.fields["selected_forms"].choices = forms_by_category
        self.fields["selected_forms"].widget.disabled_choices = disabled_choices
        self.initial["selected_forms"] = [
            e for e in self.initial["selected_forms"] if e not in disabled_choices
        ]

    def clean_selected_forms(self):
        selected_forms = models.Form.objects.filter(
            pk__in=self.cleaned_data["selected_forms"]
        )
        if any([form.has_exceeded_maximum_submissions() for form in selected_forms]):
            raise forms.ValidationError(selected_forms.first().max_submissions_message)
        return self.cleaned_data["selected_forms"]

    @transaction.atomic
    def save(self):
        selected_forms = models.Form.objects.filter(
            pk__in=self.cleaned_data["selected_forms"]
        )
        self.instance.set_selected_forms(selected_forms)

        return self.instance

    @transaction.atomic
    def save(self):
        selected_forms = models.Form.objects.filter(
            pk__in=self.cleaned_data["selected_forms"]
        )
        self.instance.set_selected_forms(selected_forms)

        return self.instance

    @transaction.atomic
    def save(self):
        selected_forms = models.Form.objects.filter(
            pk__in=self.cleaned_data["selected_forms"]
        )
        self.instance.set_selected_forms(selected_forms)

        return self.instance


class FormsSingleSelectForm(FormsSelectForm):
    selected_forms = forms.ChoiceField(widget=SingleFormRadioSelectWidget())

    def clean_selected_forms(self):
        selected_form = models.Form.objects.get(pk=self.cleaned_data["selected_forms"])
        if selected_form.has_exceeded_maximum_submissions():
            raise forms.ValidationError(selected_form.max_submissions_message)
        return self.cleaned_data["selected_forms"]

    @transaction.atomic
    def save(self):
        selected_form = models.Form.objects.get(pk=self.cleaned_data["selected_forms"])
        self.instance.set_selected_forms([selected_form])
        return self.instance


class FormsPriceSelectForm(forms.Form):

    selected_price = forms.ChoiceField(
        label=False, widget=SingleFormRadioSelectWidget(), required=True
    )

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        initial = {}
        if self.instance.submission_price is not None:
            initial = {
                "selected_price": self.instance.submission_price.original_price.pk
            }
        super(FormsPriceSelectForm, self).__init__(
            *args, **{**kwargs, "initial": initial}
        )
        if self.instance.status != self.instance.STATUS_DRAFT:
            self.fields["selected_price"].widget.attrs["disabled"] = "disabled"
        form_for_payment = self.instance.get_form_for_payment()

        choices = []
        for price in form_for_payment.prices.order_by("formprice"):
            choices.append((price.pk, price.str_for_choice()))
        self.fields["selected_price"].choices = choices

    @transaction.atomic
    def save(self):
        selected_price_id = self.cleaned_data["selected_price"]
        selected_price = Price.objects.get(pk=selected_price_id)
        price_data = {
            "amount": selected_price.amount,
            "currency": selected_price.currency,
            "text": selected_price.text,
        }
        current_submission_price = self.instance.get_submission_price()
        if current_submission_price is None:
            SubmissionPrice.objects.create(
                **{
                    **price_data,
                    "original_price": selected_price,
                    "submission": self.instance,
                }
            )
        else:
            current_submission_price.amount = price_data["amount"]
            current_submission_price.text = price_data["text"]
            current_submission_price.currency = price_data["currency"]
            current_submission_price.original_price = selected_price
            current_submission_price.save()

        return self.instance


class PartialValidationMixin:
    def __init__(self, *args, **kwargs):
        # Set to `False` to disable required fields validation (useful to allow saving incomplete forms)
        self.enable_required = kwargs.pop("enable_required", True)
        super().__init__(*args, **kwargs)


class FieldsForm(PartialValidationMixin, forms.Form):
    prefix = "fields"
    required_css_class = "required"

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        disable_fields = kwargs.pop("disable_fields", False)

        # Compute initial values for fields
        initial = {}
        prop_values = self.get_values()
        for prop_value in prop_values:
            initial[
                self.get_field_name(
                    prop_value.selected_form.form,
                    prop_value.field,
                )
            ] = prop_value.get_value()

        kwargs["initial"] = {**initial, **kwargs.get("initial", {})}

        super().__init__(*args, **kwargs)

        fields_per_form = defaultdict(list)
        payment_forms = set()

        # Create fields
        for form, field in self.get_fields():
            field_name = self.get_field_name(form, field)
            form_name = form.shortname if form.shortname else str(form)
            if form.requires_online_payment:
                payment_forms.add(form_name)
            if field.is_value_field():
                fields_per_form[form_name].append(
                    Field(field_name, title=field.help_text)
                )
                self.fields[field_name] = self.form_field_for_field(field)
                if field.is_mandatory:
                    self.fields[field_name].required = True
            else:
                fields_per_form[form_name].append(self.non_field_value_for_field(field))

        if disable_fields:
            for field in self.fields.values():
                field.disabled = True

        fieldsets = []
        for form_str, fieldset_fields in fields_per_form.items():
            if form_str in payment_forms:
                form_str = ""
            fieldset_fields = [form_str] + fieldset_fields
            fieldsets.append(Fieldset(*fieldset_fields))

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(*fieldsets)

    def get_field_representation(self, form, field):
        if field.is_value_field():
            return self[self.get_field_name(form, field)]
        else:
            return {
                "repr": non_value_input_type_mapping.get(field.input_type, {})(
                    field, True
                )
            }

    def get_form_fields_by_form(self):
        """
        Return a list of tuples `(Form, List[Field])` for each object type and their properties.
        """

        return [
            (
                object_type,
                [self.get_field_representation(object_type, prop) for prop in props],
            )
            for object_type, props in self.get_fields_by_form()
        ]

    def get_fields_by_form(self):
        """
        Return a list of tuples `(Form, List[Field])` for the forms selected in the
        current submission.
        """
        return self.instance.get_fields_by_form()

    def get_fields(self):
        """
        Return a list of tuples `(Form, Field)` for the current submission. They're
        used to create the form fields.
        """
        for form, fields in self.instance.get_fields_by_form():
            for field in fields:
                yield (form, field)

    def get_values(self):
        """
        Return `FieldValue` objects for the current submission. They're used to set the initial
        value of the form fields.
        """
        return self.instance.get_fields_values()

    def get_field_name(self, form, field):
        return "{}_{}".format(form.pk, field.pk)

    def form_field_for_field(self, field):
        """
        Return a Field instance for the given property. The specific class of the field is defined by
        `get_field_cls_for_field`.
        """
        field_class = get_field_cls_for_field(field)
        field_instance = field_class(**self.get_field_kwargs(field))

        return field_instance

    def non_field_value_for_field(self, field):
        try:
            input_func = non_value_input_type_mapping[field.input_type]
            return HTML(f"<div class='form-group'>{input_func(field)}</div>")
        except KeyError as e:
            raise KeyError(f"Field of type {e} is not supported.")

    def get_field_kwargs(self, prop):
        """
        Return the options used when instantiating the field for the given `prop`.
        """
        default_kwargs = {
            "required": self.enable_required and prop.is_mandatory,
            "label": prop.name,
            "help_text": prop.help_text if prop.help_text != "" else "",
        }

        extra_kwargs = {
            models.Field.INPUT_TYPE_TEXT: self.get_text_field_kwargs,
            models.Field.INPUT_TYPE_ADDRESS: self.get_address_field_kwargs,
            models.Field.INPUT_TYPE_DATE: self.get_date_field_kwargs,
            models.Field.INPUT_TYPE_NUMBER: self.get_number_field_kwargs,
            models.Field.INPUT_TYPE_FILE: self.get_file_field_kwargs,
            models.Field.INPUT_TYPE_REGEX: self.get_regex_field_kwargs,
            models.Field.INPUT_TYPE_LIST_SINGLE: self.get_list_single_field_kwargs,
            models.Field.INPUT_TYPE_LIST_MULTIPLE: self.get_list_multiple_field_kwargs,
        }

        try:
            return extra_kwargs[prop.input_type](prop, default_kwargs)
        except KeyError:
            return default_kwargs

    def get_text_field_kwargs(self, field, default_kwargs):
        return {
            **default_kwargs,
            "widget": forms.Textarea(
                attrs={
                    "rows": field.line_number_for_textarea,
                    "placeholder": ("ex: " + field.placeholder)
                    if field.placeholder != ""
                    else "",
                },
            ),
        }

    def get_regex_field_kwargs(self, field, default_kwargs):
        error_message = (
            (
                _("La saisie n'est pas conforme au format demandé (%(placeholder)s).")
                % {"placeholder": field.placeholder}
            )
            if field.placeholder
            else _("La saisie n'est pas conforme au format demandé.")
        )

        return {
            **default_kwargs,
            "widget": forms.Textarea(
                attrs={
                    "rows": 1,
                    "placeholder": ("ex: " + field.placeholder)
                    if field.placeholder != ""
                    else "",
                },
            ),
            "validators": [
                RegexValidator(
                    regex=field.regex_pattern,
                    message=error_message,
                )
            ],
        }

    def get_address_field_kwargs(self, field, default_kwargs):
        return {
            **default_kwargs,
            "widget": AddressWidget(
                autocomplete_options={
                    "single_address_field": True,
                },
                attrs={
                    "placeholder": ("ex: " + field.placeholder)
                    if field.placeholder != ""
                    else "",
                    "additional_searchtext_for_address_field": field.additional_searchtext_for_address_field
                    if field.additional_searchtext_for_address_field
                    else "",
                },
            ),
        }

    def get_date_field_kwargs(self, field, default_kwargs):
        return {
            **default_kwargs,
            "input_formats": [settings.DATE_INPUT_FORMAT],
            "widget": DatePickerInput(
                options={
                    "format": "DD.MM.YYYY",
                    "locale": "fr-CH",
                    "useCurrent": False,
                    "minDate": "1900/01/01",
                    "maxDate": "2100/12/31",
                },
                attrs={
                    "placeholder": ("ex: " + field.placeholder)
                    if field.placeholder != ""
                    else ""
                },
            ),
        }

    def get_number_field_kwargs(self, field, default_kwargs):
        return {
            **default_kwargs,
            "widget": forms.NumberInput(
                attrs={
                    "placeholder": ("ex: " + field.placeholder)
                    if field.placeholder != ""
                    else ""
                },
            ),
        }

    def get_file_field_kwargs(self, field, default_kwargs):
        file_size_mb = int(config.MAX_FILE_UPLOAD_SIZE / 1048576)
        default_help_text = (
            "Le fichier doit faire moins de "
            + str(file_size_mb)
            + " Megatoctet. Les extensions autorisées : "
            + config.ALLOWED_FILE_EXTENSIONS
        )

        return {
            **default_kwargs,
            "validators": [services.validate_file],
            "help_text": field.help_text
            if field.help_text != ""
            else default_help_text,
        }

    def get_list_single_field_kwargs(self, field, default_kwargs):
        choices = [("", "")] + [(value, value) for value in field.choices.splitlines()]

        return {
            **default_kwargs,
            "choices": choices,
        }

    def get_list_multiple_field_kwargs(self, field, default_kwargs):
        return {
            **default_kwargs,
            "choices": [(value, value) for value in field.choices.splitlines()],
            "widget": forms.CheckboxSelectMultiple(),
        }

    def save(self):
        to_geocode_addresses = []
        for form, field in self.get_fields():
            if field.is_value_field():
                self.instance.set_field_value(
                    form=form,
                    field=field,
                    value=self.cleaned_data[self.get_field_name(form, field)],
                )
            if (
                field.input_type == models.Field.INPUT_TYPE_ADDRESS
                and field.store_geometry_for_address_field
                and self.cleaned_data[self.get_field_name(form, field)]
            ):
                to_geocode_addresses.append(
                    self.cleaned_data[self.get_field_name(form, field)]
                )
        self.instance.reverse_geocode_and_store_address_geometry(to_geocode_addresses)


class AppendicesForm(FieldsForm):
    prefix = "appendices"

    def get_fields_by_form(self):
        return self.instance.get_appendices_fields_by_form()

    def get_fields(self):
        for form, fields in self.instance.get_appendices_fields_by_form():
            for field in fields:
                yield (form, field)

    def get_values(self):
        return self.instance.get_appendices_values()

    def get_field_kwargs(self, prop):
        return {
            **super().get_field_kwargs(prop),
            **{"widget": forms.ClearableFileInput},
        }


class SubmissionCreditorForm(forms.ModelForm):
    class Meta:
        model = models.Submission
        fields = ["creditor_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_contact_types = set(
            models.ContactType.objects.filter(
                form_category__in=self.instance.get_form_categories()
            ).values_list("type", flat=True)
        )

        choices = [
            (creditor_type, label)
            for creditor_type, label in self.fields["creditor_type"].choices
            if creditor_type in required_contact_types
        ]
        choices.insert(0, ("", "----"))
        self.fields["creditor_type"].choices = choices


class SubmissionContactForm(forms.ModelForm):
    required_css_class = "required"
    contact_fields = [
        "first_name",
        "last_name",
        "company_name",
        "vat_number",
        "address",
        "address",
        "city",
        "phone",
        "zipcode",
        "email",
    ]

    first_name = forms.CharField(
        max_length=150,
        label=_("Prénom"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "ex: Marcel",
            }
        ),
    )
    last_name = forms.CharField(
        max_length=100,
        label=_("Nom"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "ex: Dupond",
            }
        ),
    )
    phone = forms.CharField(
        min_length=10,
        max_length=16,
        label=_("Téléphone"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "ex: 024 111 22 22",
            }
        ),
        validators=[
            RegexValidator(
                regex=r"^(((\+41)\s?)|(0))?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$",
                message=mark_safe(
                    'Veuillez saisir un <a target="_blank" href="https://www.bakom.admin.ch/bakom/fr/page-daccueil/telecommunication/numerotation-et-telephonie.html">numéro de téléphone suisse valide</a>.'
                ),
            )
        ],
    )
    email = forms.EmailField(
        max_length=100,
        label=_("Email"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "ex: exemple@exemple.com",
            }
        ),
    )
    address = forms.CharField(
        max_length=100,
        label=_("Adresse"),
        widget=AddressWidget(
            autocomplete_options={
                "single_address_field": False,
                "single_contact": False,
            },
        ),
    )

    zipcode = forms.IntegerField(
        label=_("NPA"),
        validators=[MinValueValidator(1000), MaxValueValidator(9999)],
        widget=forms.NumberInput(),
    )
    city = forms.CharField(
        max_length=100,
        label=_("Ville"),
        widget=forms.TextInput(
            attrs={
                "placeholder": "ex: Yverdon",
            }
        ),
    )
    company_name = forms.CharField(
        required=False,
        label=_("Raison sociale"),
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "ex: Construction SA"}),
    )
    vat_number = forms.CharField(
        required=False,
        label=_("Numéro TVA"),
        max_length=19,
        validators=[
            RegexValidator(
                regex=r"^(CHE-)\d{3}\.\d{3}\.\d{3}(\sTVA)?$",
                message="Le code d'entreprise doit être de type \
                         CHE-123.456.789 (TVA) \
                         et vous pouvez le trouver sur \
                         le registre fédéral des entreprises \
                         https://www.uid.admin.ch/search.aspx",
            )
        ],
        widget=forms.TextInput(attrs={"placeholder": "ex: CHE-123.456.789 (TVA)"}),
    )

    class Meta:
        model = models.SubmissionContact
        fields = ["contact_type"]
        widgets = {
            "contact_type": forms.Select(
                attrs={"readonly": "readonly", "class": "hide-arrow"}
            ),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")

        if instance and instance.pk:
            kwargs["initial"] = {
                **kwargs.get("initial", {}),
                **{
                    **kwargs.get("initial", {}),
                    **{
                        field: getattr(instance.contact, field)
                        for field in self.contact_fields
                    },
                    **{"actor_type": instance.contact_type},
                },
            }

        super().__init__(*args, **kwargs)

    @transaction.atomic
    def save(self, submission, commit=True):
        contact = self.instance.contact if self.instance.pk else None

        if not contact:
            contact = models.Contact.objects.create(
                **{field: self.cleaned_data.get(field) for field in self.contact_fields}
            )
        else:
            for field in self.contact_fields:
                setattr(contact, field, self.cleaned_data.get(field))
            contact.save()

        instance = super().save(commit=False)
        instance.contact = contact
        instance.submission = submission
        instance.save()

        return instance


class SubmissionAdditionalInformationForm(forms.ModelForm):
    required_css_class = "required"

    notify_author = forms.BooleanField(
        label=_("Notifier l'auteur de la demande"),
        required=False,
    )
    reason = forms.CharField(
        label=_("Raison"),
        widget=forms.Textarea(attrs={"rows": 1}),
        required=False,
        help_text=_("(Optionnel) Raison du changement du statut de la demande"),
    )

    class Meta:
        model = models.Submission
        fields = [
            "is_public",
            "shortname",
            "status",
        ]
        widgets = {
            "is_public": forms.RadioSelect(
                choices=PUBLIC_TYPE_CHOICES,
            ),
        }

    def __init__(self, user, *args, **kwargs):
        self.instance = kwargs.get("instance", None)
        initial = {}
        for prop_value in self.get_values():
            initial[
                self.get_field_name(
                    prop_value.form.form_id,
                    prop_value.field_id,
                )
            ] = prop_value.value
        kwargs["initial"] = {**initial, **kwargs.get("initial", {})}
        super().__init__(*args, **kwargs)

        if self.instance:
            available_statuses_for_administrative_entity = list(
                models.SubmissionWorkflowStatus.objects.get_statuses_for_administrative_entity(
                    self.instance.administrative_entity
                )
            )

            # Add STATUS_INQUIRY_IN_PROGRESS when any form of submission can be STATUS_INQUIRY_IN_PROGRESS
            permanent_publication_enabled = self.instance.forms.filter(
                permanent_publication_enabled=False
            ).exists()
            if not permanent_publication_enabled:
                STATUS_INQUIRY_IN_PROGRESS = (
                    models.Submission.STATUS_INQUIRY_IN_PROGRESS
                )
            else:
                STATUS_INQUIRY_IN_PROGRESS = None

            # If an amend property in the submission can always be amended, some statuses are added to the list
            if permissions.can_always_be_updated(user, self.instance):
                filter1 = [
                    tup
                    for tup in models.Submission.STATUS_CHOICES
                    if any(i in tup for i in models.Submission.AMENDABLE_STATUSES)
                    or models.Submission.STATUS_APPROVED in tup
                    or models.Submission.STATUS_REJECTED in tup
                    or STATUS_INQUIRY_IN_PROGRESS in tup
                ]
            else:
                filter1 = [
                    tup
                    for tup in models.Submission.STATUS_CHOICES
                    if any(i in tup for i in models.Submission.AMENDABLE_STATUSES)
                    # Add curent status even if this one cannot be changed (otherwise the wrong status is selected in the disabled dropdown)
                    or self.instance.status in tup or STATUS_INQUIRY_IN_PROGRESS in tup
                ]

            filter2 = [
                el
                for el in filter1
                if any(i in el for i in available_statuses_for_administrative_entity)
            ]

            self.fields["status"].choices = tuple(filter2)
            # A permit that is approved, rejected or archived cannot have its status changed and author cannot be notified anymore
            if self.instance.status not in models.Submission.EDITABLE_STATUSES:
                self.fields["status"].disabled = True
                self.fields["notify_author"].disabled = True
                if permissions.can_always_be_updated(user, self.instance):
                    all_statuses_tuple = [
                        tup
                        for tup in models.Submission.STATUS_CHOICES
                        if any(
                            i in tup
                            for i in available_statuses_for_administrative_entity
                        )
                    ]

                    self.fields["status"].choices = tuple(all_statuses_tuple)

            # A permit that is anonymous cannot be notified
            if self.instance.forms.filter(is_anonymous=True).exists():
                self.fields["notify_author"].disabled = True

            if not config.ENABLE_GEOCALENDAR:
                self.fields["shortname"].widget = forms.HiddenInput()
                self.fields["is_public"].widget = forms.HiddenInput()

            # Only show permanent publication button if all forms have it set to True
            if (
                not self.instance.forms.filter(
                    permanent_publication_enabled=True
                ).count()
                == self.instance.forms.count()
            ):
                self.fields["is_public"].widget = forms.HiddenInput()

            for form, field in self.get_fields():
                field_name = self.get_field_name(form.id, field.id)
                self.fields[field_name] = forms.CharField(
                    label=field.name,
                    required=field.is_mandatory,
                    widget=forms.Textarea(attrs={"rows": 3}),
                )

    def get_field_name(self, form_id, field_id):
        return "{}_{}".format(form_id, field_id)

    def get_fields(self):
        """
        Return a list of tuples `(Form, SubmissionAmendField)` for the
        amend fields of the current submission. Used to create the form fields.
        """
        fields_by_form = self.instance.get_amend_custom_fields_by_form()
        for form, fields in fields_by_form:
            for field in fields:
                yield (form, field)

    def get_values(self):
        """
        Return a queryset of `SubmissionAmendFieldValue` for the custom properties
        on the current submission. They're used to set the initial value of the form
        fields.
        """
        return self.instance.get_amend_custom_fields_values()

    def get_fields_by_form(self):
        """
        Return a list of tuples `(Form, List[Field])` for each form and their fields.
        """
        return [
            (
                form,
                [self[self.get_field_name(form.id, field.id)] for field in fields],
            )
            for form, fields in self.instance.get_amend_custom_fields_by_form()
        ]

    def get_base_fields(self):
        """
        Return a list of base fields for the current Model Form.
        """
        return [self[field] for field in self.base_fields]

    def clean_status(self):
        status = self.cleaned_data.get("status")

        if (
            self.instance.status == models.Submission.STATUS_INQUIRY_IN_PROGRESS
            and not status == models.Submission.STATUS_INQUIRY_IN_PROGRESS
        ):
            raise ValidationError(
                _(
                    "Vous ne pouvez pas changer le status de la demande car une enquête public est en cours"
                )
            )

        return status

    def clean_notify_author(self):
        notify_author = self.cleaned_data.get("notify_author")

        if (
            self.cleaned_data.get("status")
            == models.Submission.STATUS_AWAITING_SUPPLEMENT
            and not notify_author
        ):
            raise ValidationError(
                _("Vous devez notifier l'auteur pour une demande de compléments")
            )

        return notify_author

    def clean_reason(self):
        reason = self.cleaned_data.get("reason")

        if (
            self.cleaned_data.get("status")
            == models.Submission.STATUS_AWAITING_SUPPLEMENT
            and self.cleaned_data.get("notify_author")
            and not reason
        ):
            raise ValidationError(
                _("Vous devez fournir une raison pour la demande de compléments")
            )

        return reason

    def save(self, commit=True):
        submission = super().save(commit=False)
        for form, field in self.get_fields():
            self.instance.set_amend_custom_field_value(
                form=form,
                field=field,
                value=self.cleaned_data[self.get_field_name(form.id, field.id)],
            )
        if commit:
            if self.cleaned_data.get("notify_author"):
                self._notify_author(submission)
            submission.save()
        return submission

    def _notify_author(self, submission):
        sender_name = (
            f"{submission.administrative_entity.expeditor_name} "
            if submission.administrative_entity.expeditor_name
            else ""
        )
        sender = (
            f"{sender_name}<{submission.administrative_entity.expeditor_email}>"
            if submission.administrative_entity.expeditor_email
            else settings.DEFAULT_FROM_EMAIL
        )

        services.send_email(
            template="submission_changed.txt",
            sender=sender,
            receivers=[submission.author.email],
            subject="{} ({})".format(
                _("Votre demande/annonce a changé de statut"),
                submission.get_forms_names_list(),
            ),
            context={
                "status": dict(submission.STATUS_CHOICES)[submission.status],
                "reason": (
                    self.cleaned_data.get("reason")
                    if self.cleaned_data.get("reason")
                    else ""
                ),
                "submission_url": submission.get_absolute_url(
                    reverse(
                        "submissions:submission_detail",
                        kwargs={"submission_id": submission.pk},
                    )
                ),
                "administrative_entity": submission.administrative_entity,
                "name": submission.author.get_full_name(),
            },
        )


# extend django gis osm openlayers widget
class GeometryWidget(geoforms.OSMWidget):
    template_name = "geometrywidget/geometrywidget.html"
    map_srid = 2056

    @property
    def media(self):
        return forms.Media(
            css={
                "all": (
                    "libs/js/openlayers6/ol.css",
                    "customWidgets/RemoteAutocomplete/remoteautocomplete.css",
                    "libs/js/jquery-ui-custom/jquery-ui.min.css",
                    "css/geotime.css",
                )
            },
            js=(
                "libs/js/openlayers6/ol.js",
                "libs/js/proj4js/proj4-src.js",
                "customWidgets/GeometryWidget/geometrywidget.js",
                "libs/js/jquery-ui-custom/jquery-ui.js",
            ),
        )


class SubmissionGeoTimeForm(forms.ModelForm):
    required_css_class = "required"
    starts_at = forms.DateTimeField(
        label=_("Date de début"),
        input_formats=[settings.DATETIME_INPUT_FORMAT],
        widget=DateTimePickerInput(
            options={
                "format": "DD.MM.YYYY HH:mm",
                "locale": "fr-CH",
                "useCurrent": False,
            },
            attrs={"autocomplete": "off"},
        ).start_of("event days"),
        help_text="Cliquer sur le champ et sélectionner la date de début à l'aide de l'outil mis à disposition",
    )
    ends_at = forms.DateTimeField(
        label=_("Date de fin"),
        input_formats=[settings.DATETIME_INPUT_FORMAT],
        widget=DateTimePickerInput(
            options={
                "format": "DD.MM.YYYY HH:mm",
                "locale": "fr-CH",
                "useCurrent": False,
            },
            attrs={"autocomplete": "off"},
        ).end_of("event days"),
        help_text="Cliquer sur le champ et sélectionner la date de fin à l'aide de l'outil mis à disposition",
    )

    class Meta:

        model = models.SubmissionGeoTime
        fields = [
            "geom",
            "starts_at",
            "ends_at",
            "comment",
            "external_link",
        ]
        help_texts = {
            "starts_at": "Date de début du chantier ou d'occupation du territoire. Si l'heure n'est pas pertinente, insérer 00:00.",
            "ends_at": "Date de fin du chantier ou d'occupation du territoire. Si l'heure n'est pas pertinente, insérer 23:59.",
        }
        widgets = {
            "geom": AdvancedGeometryWidget(),
            "comment": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        self.submission = kwargs.pop("submission", None)
        disable_fields = kwargs.pop("disable_fields", False)
        initial = {}
        if (
            self.submission.prolongation_date
            and self.submission.prolongation_status
            == self.submission.PROLONGATION_STATUS_APPROVED
        ):
            initial["ends_at"] = self.submission.prolongation_date

        kwargs["initial"] = {**initial, **kwargs.get("initial", {})}

        super().__init__(*args, **kwargs)

        required_info = self.submission.get_geotime_required_info()

        if (
            models.GeoTimeInfo.DATE not in required_info
            or self.instance.comes_from_automatic_geocoding
        ):
            del self.fields["starts_at"]
            del self.fields["ends_at"]
        if (
            models.GeoTimeInfo.GEOMETRY not in required_info
            and not self.instance.comes_from_automatic_geocoding
        ):
            del self.fields["geom"]

        # else:
        #     self.fields["geom"].widget.attrs["options"] = self.get_widget_options(
        #         self.submission
        #     )
        #     self.fields["geom"].widget.attrs["options"][
        #         "edit_geom"
        #     ] = not disable_fields
        if (
            not config.ENABLE_GEOCALENDAR
            or self.instance.comes_from_automatic_geocoding
            or (
                (models.GeoTimeInfo.GEOMETRY and models.GeoTimeInfo.DATE)
                not in required_info
            )
        ):
            del self.fields["comment"]
            del self.fields["external_link"]
        if disable_fields:
            for field in self.fields.values():
                field.disabled = True

        min_start_date = self.submission.get_min_starts_at()
        if self.fields.get("starts_at"):
            # starts_at >= min_start_date
            self.fields["starts_at"].widget.config["options"].update(
                {"minDate": min_start_date.strftime("%Y/%m/%d")}
            )
            # ends_at >= starts_at
            self.fields["ends_at"].widget.config["options"].update(
                {"minDate": min_start_date.strftime("%Y/%m/%d")}
            )

    def get_widget_options(self, submission):
        forms = submission.forms.order_by("-wms_layers_order") if submission else []

        wms_layers = [
            form.wms_layers.strip() for form in forms if form.wms_layers != ""
        ]

        forms_set = {form for form in forms}
        has_geom = any(form.has_geometry for form in forms_set)
        has_geom_point = any(form.has_geometry_point for form in forms_set)
        has_geom_line = any(form.has_geometry_line for form in forms_set)
        has_geom_polygon = any(form.has_geometry_polygon for form in forms_set)

        ftsearch_additional_searchtext_for_address_field = (
            submission.administrative_entity.additional_searchtext_for_address_field
            if submission
            else ""
        )
        options = {
            "administrative_entity_url": reverse(
                "submissions:administrative_entities_geojson",
                kwargs={
                    "administrative_entity_id": submission.administrative_entity_id
                },
            )
            if submission
            else None,
            "administrative_entity_id": submission.administrative_entity_id
            if submission
            else None,
            "wms_layers": wms_layers,
            "map_width": "100%",
            "map_height": 400,
            "default_center": [2539057, 1181111],
            "default_zoom": 10,
            "display_raw": False,
            "edit_geom": has_geom,
            "edit_point": has_geom_point,
            "edit_line": has_geom_line,
            "edit_polygon": has_geom_polygon,
            "min_zoom": 5,
            "wmts_capabilities_url": settings.WMTS_GETCAP,
            "wmts_layer": settings.WMTS_LAYER,
            "wmts_capabilities_url_alternative": settings.WMTS_GETCAP_ALTERNATIVE,
            "wmts_layer_alternative": settings.WMTS_LAYER_ALTERNATIVE,
            "restriction_area_enabled": True,
            "geometry_db_type": "GeometryCollection",
            "ftsearch_additional_searchtext_for_address_field": ftsearch_additional_searchtext_for_address_field,
            "ftsearch_apiurl": settings.LOCATIONS_SEARCH_API,
            "ftsearch_apiurl_detail": settings.LOCATIONS_SEARCH_API_DETAILS,
            "ftsearch_apiurl_origins": "address,parcel",
        }

        return options

    def clean(self):
        cleaned_data = super().clean()
        starts_at = cleaned_data.get("starts_at")
        ends_at = cleaned_data.get("ends_at")
        if starts_at and ends_at:
            if ends_at <= starts_at:
                raise ValidationError(
                    _("La date de fin doit être postérieure à la date de début.")
                )

            min_starts_at = self.submission.get_min_starts_at()
            # add two hours of tolerance in the validation
            if starts_at <= min_starts_at - timedelta(hours=2):
                raise ValidationError(
                    {
                        "starts_at": _(
                            "La date de début doit être postérieure à %(date)s"
                        )
                        % {"date": min_starts_at.strftime("%d.%m.%Y %H:%M")}
                    }
                )

            if self.submission.max_validity is not None:
                max_ends_at = starts_at + timedelta(days=self.submission.max_validity)
                if ends_at > max_ends_at + timedelta(hours=2):
                    raise ValidationError(
                        {
                            "ends_at": _(
                                "La date de fin doit être au maximum: %(date)s"
                            )
                            % {"date": max_ends_at.strftime("%d.%m.%Y %H:%M")}
                        }
                    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.submission = self.submission

        if commit:
            instance.save()

        return instance


class ModelMultipleChoiceFieldWithShortname(forms.ModelMultipleChoiceField):
    """
    Override label_from_instance to use shortname of object
    instead of __str__ method from object
    """

    def label_from_instance(self, obj):
        return obj.shortname if obj.shortname else obj


class SubmissionValidationDepartmentSelectionForm(forms.Form):
    departments = ModelMultipleChoiceFieldWithShortname(
        queryset=PermitDepartment.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        label=_("Services chargés de la validation"),
    )

    def __init__(self, instance, *args, **kwargs):
        self.submission = instance
        permit_request_ct = ContentType.objects.get_for_model(models.Submission)
        validate_permission = Permission.objects.get(
            codename="validate_submission", content_type=permit_request_ct
        )
        submission_departments = PermitDepartment.objects.filter(
            administrative_entity=self.submission.administrative_entity,
            group__permissions=validate_permission,
        ).distinct()
        departments = []
        for validation in self.submission.validations.all():
            departments.append(validation.department)
        kwargs["initial"] = dict(
            kwargs.get("initial", {}),
            departments=departments
            if departments
            else submission_departments.filter(is_default_validator=True),
        )

        super().__init__(*args, **kwargs)
        self.fields["departments"].queryset = submission_departments


class SubmissionValidationForm(forms.ModelForm):
    class Meta:
        model = models.SubmissionValidation
        fields = [
            "validation_status",
            "comment_before",
            "comment_during",
            "comment_after",
        ]
        widgets = {
            "validation_status": forms.RadioSelect(),
            "comment_before": forms.Textarea(attrs={"rows": 3}),
            "comment_during": forms.Textarea(attrs={"rows": 3}),
            "comment_after": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["validation_status"].choices = [
            (
                value,
                label,
            )
            for value, label in self.fields["validation_status"].choices
        ]


class SubmissionValidationPokeForm(forms.Form):
    def __init__(self, instance, request, *args, **kwargs):
        self.submission = instance
        self.request = request

        super().__init__(*args, **kwargs)

    def save(self):
        return services.send_validation_reminder(
            self.submission, absolute_uri_func=self.request.build_absolute_uri
        )


class SubmissionProlongationForm(forms.ModelForm):
    prolongation_date = forms.DateTimeField(
        label=_("Nouvelle date de fin demandée"),
        input_formats=[settings.DATETIME_INPUT_FORMAT],
        widget=DateTimePickerInput(
            options={
                "format": "DD.MM.YYYY HH:mm",
                "locale": "fr-CH",
                "useCurrent": False,
                "minDate": (datetime.today()).strftime("%Y/%m/%d"),
            }
        ).start_of("event days"),
        help_text="Cliquer sur le champ et sélectionner la nouvelle date de fin planifiée",
    )

    class Meta:
        model = models.Submission
        fields = [
            "prolongation_date",
            "prolongation_comment",
            "prolongation_status",
        ]
        widgets = {
            "prolongation_comment": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        prolongation_date = cleaned_data.get("prolongation_date")
        original_end_date = self.instance.get_geotime_objects().aggregate(
            Max("ends_at")
        )["ends_at__max"]

        if prolongation_date:
            if prolongation_date <= original_end_date:
                raise forms.ValidationError(
                    _(
                        "La date de prolongation doit être postérieure à la date originale de fin (%s)."
                    )
                    % original_end_date.strftime(settings.DATETIME_INPUT_FORMAT)
                )


class SubmissionClassifyForm(forms.ModelForm):
    # Status field is set as initial value when instantiating the form in the view
    status = forms.ChoiceField(
        choices=(
            (status, label)
            for status, label in models.Submission.STATUS_CHOICES
            if status
            in [
                models.Submission.STATUS_APPROVED,
                models.Submission.STATUS_REJECTED,
            ]
        ),
        widget=forms.HiddenInput,
        disabled=True,
    )

    class Meta:
        model = models.Submission
        fields = [
            "status",
            "validation_pdf",
            "additional_decision_information",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.is_validation_document_required():
            del self.fields["validation_pdf"]

    def save(self, commit=True):
        submission = super().save(commit=False)

        # ModelForm doesn't set the status because the field is disabled, so let's do it manually
        if self.cleaned_data["status"]:
            submission.status = self.cleaned_data["status"]

        submission.validated_at = timezone.now()

        if commit:
            submission.save()

        return submission


class SubmissionComplementaryDocumentsForm(forms.ModelForm):
    authorised_departments = forms.ModelMultipleChoiceField(
        queryset=None,
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
    generate_from_model = forms.ChoiceField(
        # choices=[], # dynamically populated in __init__
        required=False,
        label=_("Générer à partir du modèle"),
    )

    class Meta:
        model = models.SubmissionComplementaryDocument
        fields = [
            "generate_from_model",
            "document",
            "description",
            "status",
            "authorised_departments",
            "document_type",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, request, submission, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.request = request
        self.submission = submission
        self.fields[
            "authorised_departments"
        ].queryset = PermitDepartment.objects.filter(
            administrative_entity=submission.administrative_entity
        ).all()
        self.fields["authorised_departments"].label = _("Département autorisé")

        # TOFIX: reports that are linked to transaction should not
        # be able to be generated here but rather through the transactions' tab
        # For now, we have to get the last transaction, in order for the reports
        # linked payments to work.
        last_transaction = self.submission.get_last_transaction()

        # TODO: prefetch (to optimize reduce requests count)
        choices = [("", _("Aucune sélection"))]
        for form in self.submission.forms.all():
            subchoices = []
            parent_doc_types = form.document_types.all()
            for parent_doc_type in parent_doc_types:
                doc_types = parent_doc_type.children.all()
                for doc_type in doc_types:
                    for report in doc_type.reports.filter(is_visible=True):
                        if last_transaction is not None:
                            subchoices.append(
                                (
                                    f"{form.pk}/{report.pk}/{doc_type.pk}/{last_transaction.pk}",
                                    f"{report} / {doc_type}",
                                )
                            )
                        else:
                            subchoices.append(
                                (
                                    f"{form.pk}/{report.pk}/{doc_type.pk}/0",
                                    f"{report} / {doc_type}",
                                )
                            )
            if subchoices:
                choices.append((f"{form}", subchoices))
        self.fields["generate_from_model"].choices = choices

        parent_types = models.ComplementaryDocumentType.objects.filter(
            form__in=submission.forms.all()
        ).all()

        self.fields["document_type"].queryset = parent_types

        # Document, document type are not required, as user can also use a generated report
        self.fields["document_type"].required = False
        self.fields["document"].required = False

        for parent in parent_types:
            name = "parent_{}".format(parent.pk)
            self.fields[name] = forms.ModelChoiceField(
                queryset=models.ComplementaryDocumentType.objects.filter(
                    form=None, parent=parent
                ),
                required=False,
            )
            self.fields[name].widget.attrs["hidden"] = ""
            self.fields[name].widget.attrs["class"] = "child-type"
            self.fields[name].label = ""

    def save(self, commit=True):
        document = super().save(commit=False)
        # TODO: move logic to model
        # Backoffice uploads are stored together in dedicated structure and regrouped by permit_request ID
        document.document.field.upload_to = (
            f"backoffice_uploads/{document.submission_id}"
        )
        # set the child type as the documents type
        document.document_type = models.ComplementaryDocumentType.objects.filter(
            pk=self.cleaned_data[
                "parent_{}".format(self.cleaned_data["document_type"].pk)
            ].pk
        ).get()

        if commit:
            document.save()

        return document

    def clean_document(self):
        document = self.cleaned_data.get("document")

        # Document is not required, as user can also use a generated report
        if document:
            services.validate_file(document)

        return document

    def clean(self):
        cleaned_data = super().clean()

        # TODO: validation errors raised here don't appear in the template

        if not self.cleaned_data.get(
            "authorised_departments"
        ) and not self.cleaned_data.get("is_public"):
            raise ValidationError(
                _(
                    "Un département doit être renseigner ou le document doit être publique"
                )
            )

        if self.cleaned_data.get("document") and self.cleaned_data.get(
            "generate_from_model"
        ):
            raise ValidationError(
                _(
                    "Vous pouvez soit uploader un fichier, soit générer un document à partir d'un modèle, mais pas les deux."
                )
            )

        if not self.cleaned_data.get("document") and not self.cleaned_data.get(
            "generate_from_model"
        ):
            raise ValidationError(
                _(
                    "Vous devez soit uploader un fichier, soit générer un document à partir d'un modèle."
                )
            )

        # If document is null, it must be because we use a preset
        if not cleaned_data.get("document"):
            generate_from_model = cleaned_data.get("generate_from_model")
            try:
                (
                    form_pk,
                    report_pk,
                    child_doc_type_pk,
                    transaction_pk,
                ) = generate_from_model.split("/")
            except ValueError:
                raise ValidationError(
                    _("Selection invalide pour génération à partir du modèle !")
                )

            kwargs = {
                "form_id": form_pk,
                "report_id": report_pk,
            }
            if self.submission.get_transactions():
                rel_transaction = (
                    self.submission.get_transactions().filter(pk=transaction_pk).last()
                )
                if rel_transaction is not None:
                    kwargs.update({"transaction_id": rel_transaction.pk})
            report_response = generate_report_pdf_as_response(
                self.request.user, self.submission.pk, **kwargs
            )
            cleaned_data["document"] = File(
                io.BytesIO(b"".join(report_response.streaming_content)),
                name=report_response.filename,
            )
            # TODO CRITICAL: ensure user has access to these objects
            # •To be filtered by user
            child_doc_type = models.ComplementaryDocumentType.objects.get(
                pk=child_doc_type_pk
            )
            cleaned_data["document_type"] = child_doc_type
            cleaned_data[f"parent_{child_doc_type.pk}"] = child_doc_type.parent

        if not self.cleaned_data.get("document_type"):
            return cleaned_data

        if not cleaned_data["parent_{}".format(cleaned_data.get("document_type").pk)]:
            raise ValidationError(_("Un sous-type doit être renseigné!"))

        return cleaned_data


class AnonymousRequestForm(forms.Form):
    required_css_class = "required"
    captcha = CaptchaField(required=True)


class SubmissionInquiryForm(forms.ModelForm):
    start_date = forms.DateField(
        label=_("Date de début"),
        input_formats=[settings.DATE_INPUT_FORMAT],
        widget=DatePickerInput(
            options={
                "format": "DD.MM.YYYY",
                "locale": "fr-CH",
                "useCurrent": False,
            }
        ),
    )
    end_date = forms.DateField(
        label=_("Date de fin"),
        input_formats=[settings.DATE_INPUT_FORMAT],
        widget=DatePickerInput(
            options={
                "format": "DD.MM.YYYY",
                "locale": "fr-CH",
                "useCurrent": False,
            }
        ),
    )

    class Meta:
        model = models.SubmissionInquiry
        fields = ["start_date", "end_date", "documents"]

    def __init__(self, submission, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.submission = submission
        self.fields[
            "documents"
        ].queryset = models.SubmissionComplementaryDocument.objects.filter(
            submission=submission
        ).all()
        self.fields["documents"].help_text = _(
            "Attention, les documents non-publics seront public une fois la mise en consultation publique démarrée!"
        )

    def clean_start_date(self):
        start_date = self.cleaned_data.get("start_date")

        if start_date and start_date < datetime.today().date():
            raise ValidationError(
                _("La date de début doit être postérieure à la date d'aujourd'hui.")
            )

        return start_date

    def clean(self):
        cleaned_data = super().clean()
        start_date = self.cleaned_data.get("start_date")
        end_date = self.cleaned_data.get("end_date")

        if not start_date:
            return cleaned_data

        if end_date < start_date:
            raise ValidationError(
                _("La date de fin doit être postérieure à la date de début.")
            )

        overlap = models.SubmissionInquiry.objects.filter(
            Q(submission=self.submission)
            & Q(end_date__gte=start_date)
            & Q(start_date__lte=end_date)
        )
        if overlap and not self.instance.pk:
            raise ValidationError(
                _("Une enquête est déjà en cours pendant cette période")
            )

        return cleaned_data

    def save(self, commit=True):
        inquiry = super().save(commit=False)

        # insure all the documents added to the inquiry are public
        # if, not, make them public
        for document in self.cleaned_data["documents"]:
            if document.is_public:
                continue

            document.is_public = True
            document.save()

        if commit:
            inquiry.save()
            self.save_m2m()

        return inquiry


def get_submission_contacts_formset_initiated(submission, data=None):
    """
    Return PermitActorFormSet with initial values set
    """

    # Queryset with all configured contact types for this submission
    configured_contact_types = submission.get_contacts_types()

    # Get contact types that are not filled yet for the submission
    missing_contact_types = submission.filter_only_missing_contact_types(
        configured_contact_types
    )

    contact_initial_forms = [
        {"contact_type": contact_type[0]} for contact_type in missing_contact_types
    ]

    SubmissionContactFormset = modelformset_factory(
        models.SubmissionContact,
        form=SubmissionContactForm,
        extra=len(contact_initial_forms),
    )

    formset = SubmissionContactFormset(
        initial=contact_initial_forms,
        queryset=models.SubmissionContact.objects.filter(
            submission=submission
        ).select_related("contact"),
        data=data,
    )

    mandatory_contact_types = {
        contact_type
        for contact_type, is_mandatory in configured_contact_types
        if is_mandatory
    }

    for form in formset:
        form.empty_permitted = (
            "contact_type" not in form.initial
            or form.initial["contact_type"] not in mandatory_contact_types
        )

    return formset


def get_submission_forms(submission):
    fields_form = FieldsForm(instance=submission)
    appendices_form = AppendicesForm(instance=submission)
    fields_by_object_type = dict(fields_form.get_form_fields_by_form())
    appendices_by_object_type = dict(appendices_form.get_form_fields_by_form())
    amend_custom_fields_values = submission.get_amend_custom_fields_values()
    amend_custom_properties_by_object_type = defaultdict(list)
    for value in amend_custom_fields_values:
        amend_custom_properties_by_object_type[value.form.form].append(value)
    forms_infos = [
        (
            selected_form.form,
            fields_by_object_type.get(selected_form.form, []),
            appendices_by_object_type.get(selected_form.form, []),
            amend_custom_properties_by_object_type[selected_form.form],
        )
        for selected_form in submission.selected_forms.all()
    ]

    return forms_infos
