import json
from collections import defaultdict
from datetime import datetime, timedelta
from itertools import groupby

from allauth.socialaccount.forms import SignupForm
from allauth.socialaccount.providers.base import ProviderException
from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput
from captcha.fields import CaptchaField
from constance import config
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Field, Fieldset, Layout
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.gis import forms as geoforms
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import transaction
from django.db.models import Q, Max
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from accounts.dootix.adapter import DootixSocialAccountAdapter
from accounts.dootix.provider import DootixProvider
from accounts.geomapfish.adapter import GeomapfishSocialAccountAdapter
from accounts.geomapfish.provider import GeomapfishProvider

from . import models, services

input_type_mapping = {
    models.WorksObjectProperty.INPUT_TYPE_TEXT: forms.CharField,
    models.WorksObjectProperty.INPUT_TYPE_CHECKBOX: forms.BooleanField,
    models.WorksObjectProperty.INPUT_TYPE_NUMBER: forms.FloatField,
    models.WorksObjectProperty.INPUT_TYPE_FILE: forms.FileField,
    models.WorksObjectProperty.INPUT_TYPE_ADDRESS: forms.CharField,
    models.WorksObjectProperty.INPUT_TYPE_DATE: forms.DateField,
    models.WorksObjectProperty.INPUT_TYPE_LIST_SINGLE: forms.ChoiceField,
    models.WorksObjectProperty.INPUT_TYPE_LIST_MULTIPLE: forms.MultipleChoiceField,
    models.WorksObjectProperty.INPUT_TYPE_REGEX: forms.CharField,
}


def _title_html_representation(prop, for_summary=False):
    base = f"<h5 class='propertyTitle'>{prop.name}</h5>"
    if not for_summary and prop.help_text:
        base = f"{base}<small>{prop.help_text}</small>"
    return base


def _file_download_html_representation(prop, for_summary=False):
    if not for_summary and prop.file_download:
        description = prop.help_text if prop.help_text else _("Télécharger le fichier")
        return f"""<strong>{ prop.name }:</strong>
            <i class="fa fa-download" aria-hidden="true"></i>
            <a class="file_download" href="{ reverse('permits:works_object_property_file_download', kwargs={'path':prop.file_download}) }" target="_blank" rel="noreferrer">{ description }</a>"""
    return ""


non_value_input_type_mapping = {
    models.WorksObjectProperty.INPUT_TYPE_TITLE: _title_html_representation,
    models.WorksObjectProperty.INPUT_TYPE_FILE_DOWNLOAD: _file_download_html_representation,
}


class AddressWidget(forms.widgets.TextInput):
    @property
    def media(self):
        return forms.Media(
            css={
                "all": (
                    "customWidgets/RemoteAutocomplete/remoteautocomplete.css",
                    "libs/js/jquery-ui-custom/jquery-ui.min.css",
                )
            },
            js=(
                "customWidgets/RemoteAutocomplete/remoteautocomplete.js",
                "libs/js/jquery-ui-custom/jquery-ui.js",
            ),
        )

    def __init__(self, attrs=None, autocomplete_options=None):
        autocomplete_options = {
            "apiurl": "https://api3.geo.admin.ch/rest/services/api/SearchServer?",
            "apiurl_detail": "https://api3.geo.admin.ch/rest/services/api/MapServer/ch.bfs.gebaeude_wohnungs_register/",
            "origins": "address",
            "zipcode_field": "zipcode",
            "city_field": "city",
            "placeholder": gettext("ex: Place Pestalozzi 2, 1400 Yverdon"),
            "single_contact": True,
            "single_address_field": False,
            **(autocomplete_options or {}),
        }
        super().__init__(
            {
                **(attrs or {}),
                "data_remote_autocomplete": json.dumps(autocomplete_options),
            }
        )


def get_field_cls_for_property(prop):
    try:
        return input_type_mapping[prop.input_type]
    except KeyError as e:
        raise KeyError(f"Field of type {e} is not supported.")


def regroup_by_ofs_id(entities):
    return groupby(entities.order_by("ofs_id"), lambda entity: entity.ofs_id)


class GroupedRadioWidget(forms.RadioSelect):
    template_name = "permits/widgets/groupedradio.html"

    class Media:
        css = {"all": ("customWidgets/GroupedRadio/groupedradio.css",)}


class AdministrativeEntityForm(forms.Form):
    administrative_entity = forms.ModelChoiceField(
        label=_("Entité administrative"),
        widget=GroupedRadioWidget(),
        queryset=models.PermitAdministrativeEntity.objects.all(),
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        self.user = kwargs.pop("user", None)
        session = kwargs.pop("session", None)
        tags = session["entityfilter"] if "entityfilter" in session else []

        if self.instance:
            initial = {
                **kwargs.get("initial", {}),
                "administrative_entity": self.instance.administrative_entity.pk,
            }
        else:
            initial = {}

        kwargs["initial"] = initial

        super().__init__(*args, **kwargs)
        entities_by_tag = services.get_administrative_entities(
            self.user
        ).filter_by_tags(tags)
        if not entities_by_tag.exists():
            session["entityfilter"] = []
        self.fields["administrative_entity"].choices = [
            (ofs_id, [(entity.pk, entity.name) for entity in entities])
            for ofs_id, entities in regroup_by_ofs_id(
                entities_by_tag
                if entities_by_tag
                else services.get_administrative_entities(self.user)
            )
        ]

    def save(self, author):
        administrative_entity_instance = models.PermitAdministrativeEntity.objects.get(
            pk=self.cleaned_data["administrative_entity"].pk
        )

        if not self.instance:
            return models.PermitRequest.objects.create(
                administrative_entity=administrative_entity_instance,
                author=author,
            )
        else:
            services.set_administrative_entity(
                self.instance, administrative_entity_instance
            )
            return self.instance


class WorksTypesForm(forms.Form):
    types = forms.ModelMultipleChoiceField(
        queryset=models.WorksType.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        label=_("Types de travaux"),
        error_messages={"required": _("Sélectionnez au moins un type de demande")},
    )

    def __init__(self, instance, *args, **kwargs):
        self.instance = instance
        self.user = kwargs.pop("user", None)
        session = kwargs.pop("session", None)
        typefilter = session["typefilter"] if "typefilter" in session else []
        kwargs["initial"] = (
            {"types": services.get_permit_request_works_types(self.instance)}
            if self.instance
            else {}
        )

        super().__init__(*args, **kwargs)
        works_types = services.get_works_types(
            self.instance.administrative_entity, self.user
        )
        if typefilter:
            if works_types.filter_by_tags(typefilter).exists():
                works_types = works_types.filter_by_tags(typefilter)
            else:
                session["typefilter"] = []
        self.fields["types"].queryset = works_types

    def save(self):
        services.set_works_types(self.instance, self.cleaned_data["types"])


class WorksObjectsTypeChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.works_object.name


class WorksObjectsForm(forms.Form):
    prefix = "works_objects"

    def __init__(self, instance, works_types, *args, **kwargs):
        self.instance = instance
        self.user = kwargs.pop("user", None)

        initial = {}
        for type_id, object_id in self.instance.works_object_types.values_list(
            "works_type__id", "id"
        ):
            initial.setdefault(str(type_id), []).append(object_id)

        super().__init__(*args, **{**kwargs, "initial": initial})
        user_has_perm = self.user.has_perm("permits.see_private_requests")
        for works_type in works_types:
            queryset = (
                works_type.works_object_types.filter(
                    administrative_entities=self.instance.administrative_entity,
                )
                .distinct()
                .select_related("works_object")
                .order_by("works_type", "works_object")
            )

            if not user_has_perm:
                queryset = queryset.filter(is_public=True)

            queryset = queryset.filter(is_anonymous=self.user.permitauthor.is_temporary)

            self.fields[str(works_type.pk)] = WorksObjectsTypeChoiceField(
                queryset=queryset,
                widget=forms.CheckboxSelectMultiple(),
                label=works_type.name,
                error_messages={
                    "required": _("Sélectionnez au moins un objet par type de demande")
                },
            )

    @transaction.atomic
    def save(self):
        works_object_types = [
            item for sublist in self.cleaned_data.values() for item in sublist
        ]

        services.set_works_object_types(self.instance, works_object_types)

        return self.instance


class PartialValidationMixin:
    def __init__(self, *args, **kwargs):
        # Set to `False` to disable required fields validation (useful to allow saving incomplete forms)
        self.enable_required = kwargs.pop("enable_required", True)
        super().__init__(*args, **kwargs)


class WorksObjectsPropertiesForm(PartialValidationMixin, forms.Form):
    prefix = "properties"
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
                    prop_value.works_object_type_choice.works_object_type,
                    prop_value.property,
                )
            ] = services.get_property_value(prop_value)

        kwargs["initial"] = {**initial, **kwargs.get("initial", {})}

        super().__init__(*args, **kwargs)

        fields_per_work_object = defaultdict(list)
        # Create a field for each property
        for works_object_type, prop in self.get_properties():
            field_name = self.get_field_name(works_object_type, prop)
            if prop.is_value_property():
                fields_per_work_object[str(works_object_type)].append(
                    Field(field_name, title=prop.help_text)
                )
                self.fields[field_name] = self.field_for_property(prop)
                if prop.is_mandatory:
                    self.fields[field_name].required = True
            else:
                fields_per_work_object[str(works_object_type)].append(
                    self.non_field_value_for_property(prop)
                )

        if disable_fields:
            for field in self.fields.values():
                field.disabled = True

        fieldsets = []
        for work_object_type_str, fieldset_fields in fields_per_work_object.items():
            fieldset_fields = [work_object_type_str] + fieldset_fields
            fieldsets.append(Fieldset(*fieldset_fields))

        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(*fieldsets)

    def get_field_representation(self, object_type, prop):
        if prop.is_value_property():
            return self[self.get_field_name(object_type, prop)]
        else:
            return {
                "repr": non_value_input_type_mapping.get(prop.input_type, {})(
                    prop, True
                )
            }

    def get_fields_by_object_type(self):
        """
        Return a list of tuples `(WorksObjectType, List[Field])` for each object type and their properties.
        """

        return [
            (
                object_type,
                [self.get_field_representation(object_type, prop) for prop in props],
            )
            for object_type, props in self.get_properties_by_object_type()
        ]

    def get_properties_by_object_type(self):
        """
        Return a list of tuples `(WorksObjectType, List[WorksObjectTypeProperty])` for the object-types selected in the
        current permit request.
        """
        return services.get_properties(self.instance)

    def get_properties(self):
        """
        Return a list of tuples `(WorksObjectType, WorksObjectTypeProperty)` for the current permit request. They're
        used to create the form fields.
        """
        return services.get_permit_request_properties(self.instance)

    def get_values(self):
        """
        Return a `WorksObjectPropertyValue` objects for the current permit request. They're used to set the initial
        value of the form fields.
        """
        return services.get_properties_values(self.instance)

    def get_field_name(self, works_object_type, prop):
        return "{}_{}".format(works_object_type.pk, prop.pk)

    def field_for_property(self, prop):
        """
        Return a Field instance for the given property. The specific class of the field is defined by
        `get_field_cls_for_property`.
        """
        field_class = get_field_cls_for_property(prop)
        field_instance = field_class(**self.get_field_kwargs(prop))

        return field_instance

    def non_field_value_for_property(self, prop):
        try:
            input_func = non_value_input_type_mapping[prop.input_type]
            return HTML(f"<div class='form-group'>{input_func(prop)}</div>")
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
            models.WorksObjectProperty.INPUT_TYPE_TEXT: self.get_text_field_kwargs,
            models.WorksObjectProperty.INPUT_TYPE_ADDRESS: self.get_address_field_kwargs,
            models.WorksObjectProperty.INPUT_TYPE_DATE: self.get_date_field_kwargs,
            models.WorksObjectProperty.INPUT_TYPE_NUMBER: self.get_number_field_kwargs,
            models.WorksObjectProperty.INPUT_TYPE_FILE: self.get_file_field_kwargs,
            models.WorksObjectProperty.INPUT_TYPE_REGEX: self.get_regex_field_kwargs,
            models.WorksObjectProperty.INPUT_TYPE_LIST_SINGLE: self.get_list_single_field_kwargs,
            models.WorksObjectProperty.INPUT_TYPE_LIST_MULTIPLE: self.get_list_multiple_field_kwargs,
        }

        try:
            return extra_kwargs[prop.input_type](prop, default_kwargs)
        except KeyError:
            return default_kwargs

    def get_text_field_kwargs(self, prop, default_kwargs):
        return {
            **default_kwargs,
            "widget": forms.Textarea(
                attrs={
                    "rows": prop.line_number_for_textarea,
                    "placeholder": ("ex: " + prop.placeholder)
                    if prop.placeholder != ""
                    else "",
                },
            ),
        }

    def get_regex_field_kwargs(self, prop, default_kwargs):
        error_message = (
            (
                _("La saisie n'est pas conforme au format demandé (%(placeholder)s).")
                % {"placeholder": prop.placeholder}
            )
            if prop.placeholder
            else _("La saisie n'est pas conforme au format demandé.")
        )

        return {
            **default_kwargs,
            "widget": forms.Textarea(
                attrs={
                    "rows": 1,
                    "placeholder": ("ex: " + prop.placeholder)
                    if prop.placeholder != ""
                    else "",
                },
            ),
            "validators": [
                RegexValidator(
                    regex=prop.regex_pattern,
                    message=error_message,
                )
            ],
        }

    def get_address_field_kwargs(self, prop, default_kwargs):
        return {
            **default_kwargs,
            "widget": AddressWidget(
                autocomplete_options={"single_address_field": True},
                attrs={
                    "placeholder": ("ex: " + prop.placeholder)
                    if prop.placeholder != ""
                    else ""
                },
            ),
        }

    def get_date_field_kwargs(self, prop, default_kwargs):
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
                    "placeholder": ("ex: " + prop.placeholder)
                    if prop.placeholder != ""
                    else ""
                },
            ),
        }

    def get_number_field_kwargs(self, prop, default_kwargs):
        return {
            **default_kwargs,
            "widget": forms.NumberInput(
                attrs={
                    "placeholder": ("ex: " + prop.placeholder)
                    if prop.placeholder != ""
                    else ""
                },
            ),
        }

    def get_file_field_kwargs(self, prop, default_kwargs):
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
            "help_text": prop.help_text if prop.help_text != "" else default_help_text,
        }

    def get_list_single_field_kwargs(self, prop, default_kwargs):
        choices = [("", "")] + [(value, value) for value in prop.choices.splitlines()]

        return {
            **default_kwargs,
            "choices": choices,
        }

    def get_list_multiple_field_kwargs(self, prop, default_kwargs):
        return {
            **default_kwargs,
            "choices": [(value, value) for value in prop.choices.splitlines()],
            "widget": forms.CheckboxSelectMultiple(),
        }

    def save(self):
        for works_object_type, prop in self.get_properties():
            if prop.is_value_property():
                services.set_object_property_value(
                    permit_request=self.instance,
                    object_type=works_object_type,
                    prop=prop,
                    value=self.cleaned_data[
                        self.get_field_name(works_object_type, prop)
                    ],
                )


class WorksObjectsAppendicesForm(WorksObjectsPropertiesForm):
    prefix = "appendices"

    def get_properties_by_object_type(self):
        return services.get_appendices(self.instance)

    def get_properties(self):
        return services.get_permit_request_appendices(self.instance)

    def get_values(self):
        return services.get_appendices_values(self.instance)

    def get_field_kwargs(self, prop):
        return {
            **super().get_field_kwargs(prop),
            **{"widget": forms.ClearableFileInput},
        }


def check_existing_email(email, user):

    if (
        User.objects.filter(email=email)
        .exclude(Q(id=user.id) if user else Q())
        .exists()
    ):
        raise ValidationError(_("Cet email est déjà utilisé."))

    return email


class NewDjangoAuthUserForm(UserCreationForm):

    first_name = forms.CharField(
        label=_("Prénom"),
        max_length=30,
    )
    last_name = forms.CharField(
        label=_("Nom"),
        max_length=150,
    )
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
    )
    required_css_class = "required"

    def clean_email(self):
        return check_existing_email(self.cleaned_data["email"], user=None)

    def clean(self):
        cleaned_data = super().clean()

        for reserved_usernames in (
            settings.TEMPORARY_USER_PREFIX,
            settings.ANONYMOUS_USER_PREFIX,
        ):
            if cleaned_data["username"].startswith(reserved_usernames):
                raise ValidationError(
                    {
                        "username": _(
                            "Le nom d'utilisat·eur·rice ne peut pas commencer par %s"
                        )
                        % reserved_usernames
                    }
                )

        if cleaned_data["first_name"] == settings.ANONYMOUS_NAME:
            raise ValidationError(
                {
                    "first_name": _("Le prénom ne peut pas être %s")
                    % settings.ANONYMOUS_NAME
                }
            )

        if cleaned_data["last_name"] == settings.ANONYMOUS_NAME:
            raise ValidationError(
                {"last_name": _("Le nom ne peut pas être %s") % settings.ANONYMOUS_NAME}
            )

        return cleaned_data

    def save(self, commit=True):
        user = super(NewDjangoAuthUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.backend = "django.contrib.auth.backends.ModelBackend"

        if commit:
            user.save()

        return user


class DjangoAuthUserForm(forms.ModelForm):
    """User"""

    first_name = forms.CharField(
        max_length=30,
        label=_("Prénom"),
        widget=forms.TextInput(
            attrs={"placeholder": "ex: Marcel", "required": "required"}
        ),
    )
    last_name = forms.CharField(
        max_length=150,
        label=_("Nom"),
        widget=forms.TextInput(
            attrs={"placeholder": "ex: Dupond", "required": "required"}
        ),
    )
    email = forms.EmailField(
        max_length=254,
        label=_("Email"),
        widget=forms.TextInput(
            attrs={"placeholder": "ex: exemple@exemple.com", "required": "required"}
        ),
    )
    required_css_class = "required"

    def clean_email(self):
        return check_existing_email(self.cleaned_data["email"], self.instance)

    def clean_first_name(self):
        if self.cleaned_data["first_name"] == settings.ANONYMOUS_NAME:
            raise ValidationError(
                _("Le prénom ne peut pas être %s") % settings.ANONYMOUS_NAME
            )

    def clean_last_name(self):
        if self.cleaned_data["last_name"] == settings.ANONYMOUS_NAME:
            raise ValidationError(
                _("Le nom ne peut pas être %s") % settings.ANONYMOUS_NAME
            )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class GenericAuthorForm(forms.ModelForm):

    required_css_class = "required"
    address = forms.CharField(
        max_length=100, label=_("Adresse"), widget=AddressWidget()
    )

    zipcode = forms.IntegerField(
        label=_("NPA"),
        validators=[MinValueValidator(1000), MaxValueValidator(9999)],
        widget=forms.NumberInput(attrs={"required": "required"}),
    )
    city = forms.CharField(
        max_length=100,
        label=_("Ville"),
        widget=forms.TextInput(
            attrs={"placeholder": "ex: Yverdon", "required": "required"}
        ),
    )

    class Meta:
        model = models.PermitAuthor
        fields = [
            "address",
            "zipcode",
            "city",
            "phone_first",
            "phone_second",
            "company_name",
            "vat_number",
            "notify_per_email",
        ]
        help_texts = {
            "vat_number": 'Trouvez votre numéro <a href="https://www.uid.admin.ch/Search.aspx?lang=fr" target="_blank">TVA</a>',
            "notify_per_email": """Permet d'activer la réception des notifications
                automatiques de suivi dans votre boîte mail, par exemple lorsqu'une
                demande a été soumise ou est en attente de validation.""",
        }
        widgets = {
            "phone_first": forms.TextInput(attrs={"placeholder": "ex: 024 111 22 22"}),
            "phone_second": forms.TextInput(attrs={"placeholder": "ex: 079 111 22 22"}),
            "vat_number": forms.TextInput(attrs={"placeholder": "ex: CHE-123.456.789"}),
            "company_name": forms.TextInput(
                attrs={"placeholder": "ex: Construction SA"}
            ),
        }


class PermitRequestCreditorForm(forms.ModelForm):
    class Meta:
        model = models.PermitRequest
        fields = ["creditor_type"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        required_actor_types = set(
            models.PermitActorType.objects.filter(
                works_type__in=services.get_permit_request_works_types(self.instance)
            ).values_list("type", flat=True)
        )

        choices = [
            (creditor_type, label)
            for creditor_type, label in self.fields["creditor_type"].choices
            if creditor_type in required_actor_types
        ]
        choices.insert(0, ("", "----"))
        self.fields["creditor_type"].choices = choices


class PermitRequestActorForm(forms.ModelForm):
    """Contacts"""

    required_css_class = "required"
    actor_fields = [
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
                         le registe fédéral des entreprises \
                         https://www.uid.admin.ch/search.aspx",
            )
        ],
        widget=forms.TextInput(attrs={"placeholder": "ex: CHE-123.456.789 (TVA)"}),
    )

    class Meta:
        model = models.PermitRequestActor
        fields = ["actor_type"]
        widgets = {
            "actor_type": forms.Select(
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
                        field: getattr(instance.actor, field)
                        for field in self.actor_fields
                    },
                    **{"actor_type": instance.actor_type},
                },
            }

        super().__init__(*args, **kwargs)

    @transaction.atomic
    def save(self, permit_request, commit=True):
        actor = self.instance.actor if self.instance.pk else None

        if not actor:
            actor = models.PermitActor.objects.create(
                **{field: self.cleaned_data.get(field) for field in self.actor_fields}
            )
        else:
            for field in self.actor_fields:
                setattr(actor, field, self.cleaned_data.get(field))
            actor.save()

        instance = super().save(commit=False)
        instance.actor = actor
        instance.permit_request = permit_request
        instance.save()

        return instance


class PermitRequestAdditionalInformationForm(forms.ModelForm):
    required_css_class = "required"

    class Meta:
        model = models.PermitRequest
        fields = ["is_public", "shortname", "status"]
        widgets = {
            "is_public": forms.RadioSelect(
                choices=models.PUBLIC_TYPE_CHOICES,
            ),
        }

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get("instance", None)

        initial = {}
        for prop_value in self.get_values():
            initial[
                self.get_field_name(
                    prop_value.works_object_type_choice.works_object_type_id,
                    prop_value.property_id,
                )
            ] = prop_value.value
        kwargs["initial"] = {**initial, **kwargs.get("initial", {})}

        super().__init__(*args, **kwargs)

        if self.instance:
            available_statuses_for_administrative_entity = list(
                services.get_status_choices_for_administrative_entity(
                    self.instance.administrative_entity
                )
            )
            # If an amend property in the permit request can always be amended, STATUS_APPROVED is added to the list
            if self.instance.get_amend_property_list_always_amendable():
                filter1 = [
                    tup
                    for tup in models.PermitRequest.STATUS_CHOICES
                    if any(i in tup for i in models.PermitRequest.AMENDABLE_STATUSES)
                    or models.PermitRequest.STATUS_APPROVED in tup
                ]
            else:
                filter1 = [
                    tup
                    for tup in models.PermitRequest.STATUS_CHOICES
                    if any(i in tup for i in models.PermitRequest.AMENDABLE_STATUSES)
                ]
            filter2 = [
                el
                for el in filter1
                if any(i in el for i in available_statuses_for_administrative_entity)
            ]
            self.fields["status"].choices = tuple(filter2)

            if not config.ENABLE_GEOCALENDAR:
                self.fields["is_public"].widget = forms.HiddenInput()
                self.fields["shortname"].widget = forms.HiddenInput()

            for works_object_type, prop in self.get_properties():
                field_name = self.get_field_name(works_object_type.id, prop.id)
                self.fields[field_name] = forms.CharField(
                    label=prop.name,
                    required=prop.is_mandatory,
                    widget=forms.Textarea(attrs={"rows": 3}),
                )

    def get_field_name(self, works_object_type_id, prop_id):
        return "{}_{}".format(works_object_type_id, prop_id)

    def get_properties(self):
        """
        Return a list of tuples `(WorksObjectType, PermitRequestAmendProperty)` for the
        amend properties of the current permit request. Used to create the form fields.
        """
        return services.get_permit_request_amend_custom_properties(self.instance)

    def get_values(self):
        """
        Return a queryset of `PermitRequestAmendPropertyValue` for the custom properties
        on the current permit request. They're used to set the initial value of the form
        fields.
        """
        return services.get_amend_custom_properties_values(self.instance)

    def get_fields_by_object_type(self):
        """
        Return a list of tuples `(WorksObjectType, List[Field])` for each object type and their properties.
        """
        return [
            (
                object_type,
                [self[self.get_field_name(object_type.id, prop.id)] for prop in props],
            )
            for object_type, props in services.get_permit_request_amend_custom_properties_by_object_type(
                self.instance
            )
        ]

    def get_base_fields(self):
        """
        Return a list of base fields for the current Model Form.
        """
        return [self[field] for field in self.base_fields]

    def save(self, commit=True):
        permit_request = super().save(commit=False)
        for works_object_type, prop in self.get_properties():
            services.set_amend_custom_property_value(
                permit_request=self.instance,
                object_type=works_object_type,
                prop=prop,
                value=self.cleaned_data[
                    self.get_field_name(works_object_type.id, prop.id)
                ],
            )
        if commit:
            permit_request.save()
        return permit_request


# extend django gis osm openlayers widget
class GeometryWidget(geoforms.OSMWidget):

    template_name = "geometrywidget/geometrywidget.html"
    map_srid = 2056

    @property
    def media(self):
        return forms.Media(
            css={"all": ("libs/js/openlayers6/ol.css", "css/geotime.css")},
            js=(
                "libs/js/openlayers6/ol.js",
                "libs/js/proj4js/proj4-src.js",
                "customWidgets/GeometryWidget/geometrywidget.js",
            ),
        )


class PermitRequestGeoTimeForm(forms.ModelForm):

    required_css_class = "required"
    starts_at = forms.DateTimeField(
        label=_("Date planifiée de début"),
        input_formats=[settings.DATETIME_INPUT_FORMAT],
        widget=DateTimePickerInput(
            options={
                "format": "DD.MM.YYYY HH:mm",
                "locale": "fr-CH",
                "useCurrent": False,
            },
            attrs={"autocomplete": "off"},
        ).start_of("event days"),
        help_text="Cliquer sur le champ et selectionner la date planifiée de début à l'aide de l'outil mis à disposition",
    )
    ends_at = forms.DateTimeField(
        label=_("Date planifiée de fin"),
        input_formats=[settings.DATETIME_INPUT_FORMAT],
        widget=DateTimePickerInput(
            options={
                "format": "DD.MM.YYYY HH:mm",
                "locale": "fr-CH",
                "useCurrent": False,
            },
            attrs={"autocomplete": "off"},
        ).end_of("event days"),
        help_text="Cliquer sur le champ et selectionner la date planifiée de fin à l'aide de l'outil mis à disposition",
    )

    class Meta:

        model = models.PermitRequestGeoTime
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
            "geom": GeometryWidget(),
            "comment": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        self.permit_request = kwargs.pop("permit_request", None)
        disable_fields = kwargs.pop("disable_fields", False)

        initial = {}
        if (
            self.permit_request.prolongation_date
            and self.permit_request.prolongation_status
            == self.permit_request.PROLONGATION_STATUS_APPROVED
        ):
            initial["ends_at"] = self.permit_request.prolongation_date

        kwargs["initial"] = {**initial, **kwargs.get("initial", {})}

        super().__init__(*args, **kwargs)

        required_info = services.get_geotime_required_info(self.permit_request)

        if services.GeoTimeInfo.DATE not in required_info:
            del self.fields["starts_at"]
            del self.fields["ends_at"]

        if services.GeoTimeInfo.GEOMETRY not in required_info:
            del self.fields["geom"]

        else:
            self.fields["geom"].widget.attrs["options"] = self.get_widget_options(
                self.permit_request
            )
            self.fields["geom"].widget.attrs["options"][
                "edit_geom"
            ] = not disable_fields
        if not config.ENABLE_GEOCALENDAR:
            del self.fields["comment"]
            del self.fields["external_link"]
        if disable_fields:
            for field in self.fields.values():
                field.disabled = True

        min_start_date = self.permit_request.get_min_starts_at()
        if self.fields.get("starts_at"):
            # starts_at >= min_start_date
            self.fields["starts_at"].widget.config["options"].update(
                {"minDate": min_start_date.strftime("%Y/%m/%d")}
            )
            # ends_at >= starts_at
            self.fields["ends_at"].widget.config["options"].update(
                {"minDate": min_start_date.strftime("%Y/%m/%d")}
            )

    def get_widget_options(self, permit_request):
        works_object_type_choices = (
            services.get_works_object_type_choices(permit_request)
            .select_related("works_object_type__works_object")
            .order_by("-works_object_type__works_object__wms_layers_order")
            if permit_request
            else []
        )

        wms_layers = [
            works_object_type_choice.works_object_type.works_object.wms_layers.strip()
            for works_object_type_choice in works_object_type_choices
            if works_object_type_choice.works_object_type.works_object.wms_layers != ""
        ]

        works_object_types = {
            choice.works_object_type for choice in works_object_type_choices
        }
        has_geom = any(
            works_object_type.has_geometry for works_object_type in works_object_types
        )
        has_geom_point = any(
            works_object_type.has_geometry_point
            for works_object_type in works_object_types
        )
        has_geom_line = any(
            works_object_type.has_geometry_line
            for works_object_type in works_object_types
        )
        has_geom_polygon = any(
            works_object_type.has_geometry_polygon
            for works_object_type in works_object_types
        )

        options = {
            "administrative_entity_url": reverse(
                "permits:administrative_entities_geojson",
                kwargs={
                    "administrative_entity_id": permit_request.administrative_entity_id
                },
            )
            if permit_request
            else None,
            "administrative_entity_id": permit_request.administrative_entity_id
            if permit_request
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
            "qgisserver_proxy": reverse("permits:qgisserver_proxy"),
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

            min_starts_at = self.permit_request.get_min_starts_at()
            # add two hours of tolerance in the validation
            if starts_at <= min_starts_at - timedelta(hours=2):
                raise ValidationError(
                    {
                        "starts_at": _(
                            "La date planifiée de début doit être postérieure à %(date)s"
                        )
                        % {"date": min_starts_at.strftime("%d.%m.%Y %H:%M")}
                    }
                )

            if self.permit_request.max_validity is not None:
                max_ends_at = starts_at + timedelta(
                    days=self.permit_request.max_validity
                )
                if ends_at > max_ends_at + timedelta(hours=2):
                    raise ValidationError(
                        {
                            "ends_at": _(
                                "La date planifiée de fin doit être au maximum: %(date)s"
                            )
                            % {"date": max_ends_at.strftime("%d.%m.%Y %H:%M")}
                        }
                    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.permit_request = self.permit_request

        if commit:
            instance.save()

        return instance


class PermitRequestValidationDepartmentSelectionForm(forms.Form):
    departments = forms.ModelMultipleChoiceField(
        queryset=models.PermitDepartment.objects.none(),
        widget=forms.CheckboxSelectMultiple(),
        label=_("Services chargés de la validation"),
    )

    def __init__(self, instance, *args, **kwargs):
        self.permit_request = instance
        permit_request_ct = ContentType.objects.get_for_model(models.PermitRequest)
        validate_permission = Permission.objects.get(
            codename="validate_permit_request", content_type=permit_request_ct
        )
        permit_request_departments = models.PermitDepartment.objects.filter(
            administrative_entity=self.permit_request.administrative_entity,
            group__permissions=validate_permission,
        ).distinct()

        departments = []
        for validation in self.permit_request.validations.all():
            departements = departments.append(validation.department)
        kwargs["initial"] = dict(
            kwargs.get("initial", {}),
            departments=departments
            if departments
            else permit_request_departments.filter(is_default_validator=True),
        )

        super().__init__(*args, **kwargs)
        self.fields["departments"].queryset = permit_request_departments


class PermitRequestValidationForm(forms.ModelForm):
    class Meta:
        model = models.PermitRequestValidation
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


class PermitRequestValidationPokeForm(forms.Form):
    def __init__(self, instance, request, *args, **kwargs):
        self.permit_request = instance
        self.request = request

        super().__init__(*args, **kwargs)

    def save(self):
        return services.send_validation_reminder(
            self.permit_request, absolute_uri_func=self.request.build_absolute_uri
        )


class PermitRequestProlongationForm(forms.ModelForm):
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
        model = models.PermitRequest
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
        original_end_date = services.get_geotime_objects(self.instance.id).aggregate(
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


class PermitRequestClassifyForm(forms.ModelForm):
    # Status field is set as initial value when instantiating the form in the view
    status = forms.ChoiceField(
        choices=(
            (status, label)
            for status, label in models.PermitRequest.STATUS_CHOICES
            if status
            in [
                models.PermitRequest.STATUS_APPROVED,
                models.PermitRequest.STATUS_REJECTED,
            ]
        ),
        widget=forms.HiddenInput,
        disabled=True,
    )

    class Meta:
        model = models.PermitRequest
        fields = [
            "is_public",
            "status",
            "validation_pdf",
            "additional_decision_information",
        ]

    def __init__(self, *args, **kwargs):
        super(PermitRequestClassifyForm, self).__init__(*args, **kwargs)
        if not services.is_validation_document_required(self.instance):
            del self.fields["validation_pdf"]

        if not config.ENABLE_GEOCALENDAR:
            del self.fields["is_public"]

    def save(self, commit=True):
        permit_request = super().save(commit=False)

        # ModelForm doesn't set the status because the field is disabled, so let's do it manually
        if self.cleaned_data["status"]:
            permit_request.status = self.cleaned_data["status"]

        permit_request.validated_at = timezone.now()

        if commit:
            permit_request.save()

        return permit_request


class PermitRequestComplementaryDocumentsForm(forms.ModelForm):
    # Add permission to pilote & other thing to upload documents
    # -> Read manual or whatever
    # Display uploaded files
    # Maybe prep for file encryption

    class Meta:
        model = models.PermitRequestComplementaryDocument
        fields = ["document", "description"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 2, "cols": 20}),
        }


class SocialSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label=_("Prénom"),
        widget=forms.TextInput(
            attrs={"placeholder": "ex: Marcel", "required": "required"}
        ),
    )
    last_name = forms.CharField(
        max_length=150,
        label=_("Nom"),
        widget=forms.TextInput(
            attrs={"placeholder": "ex: Dupond", "required": "required"}
        ),
    )

    required_css_class = "required"

    address = forms.CharField(
        max_length=100, label=_("Adresse"), widget=AddressWidget()
    )

    zipcode = forms.IntegerField(
        label=_("NPA"),
        min_value=1000,
        max_value=9999,
        widget=forms.NumberInput(attrs={"required": "required"}),
    )
    city = forms.CharField(
        max_length=100,
        label=_("Ville"),
        widget=forms.TextInput(
            attrs={"placeholder": "ex: Yverdon", "required": "required"}
        ),
    )
    phone_first = forms.CharField(
        label=_("Téléphone principal"),
        max_length=20,
        required=True,
        widget=forms.TextInput(attrs={"placeholder": "ex: 024 111 22 22"}),
        validators=[
            RegexValidator(
                regex=r"^(((\+41)\s?)|(0))?(\d{2})\s?(\d{3})\s?(\d{2})\s?(\d{2})$",
                message="Seuls les chiffres et les espaces sont autorisés.",
            )
        ],
    )

    phone_second = forms.CharField(
        required=False,
        label=_("Téléphone secondaire"),
        max_length=20,
        widget=forms.TextInput(attrs={"placeholder": "ex: 079 111 22 22"}),
    )

    company_name = forms.CharField(
        required=False,
        label=_("Raison Sociale"),
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "ex: Construction SA"}),
    )

    vat_number = forms.CharField(
        required=False,
        label=_("Numéro TVA"),
        max_length=19,
        widget=forms.TextInput(attrs={"placeholder": "ex: CHE-123.456.789"}),
        help_text=_(
            'Trouvez votre numéro <a href="https://www.uid.admin.ch/Search.aspx'
            '?lang=fr" target="_blank">TVA</a>'
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = _("Nom d’utilisateur")
        self.fields["username"].required = True
        self.fields["email"].disabled = True
        if kwargs["sociallogin"].user.username != "":
            self.fields["username"].disabled = True

    def save(self, request):
        # SOCIALACCOUNT_FORMS.signup is unique, but providers are multiple.
        # Find the correct adapter to save the new User.
        if self.sociallogin.account.provider == DootixProvider.id:
            adapter = DootixSocialAccountAdapter(request)
        elif self.sociallogin.account.provider == GeomapfishProvider.id:
            adapter = GeomapfishSocialAccountAdapter(request)
        else:
            raise ProviderException(_("Unknown social account provider"))

        return adapter.save_user(request, self.sociallogin, form=self)


class AnonymousRequestForm(forms.Form):
    required_css_class = "required"
    captcha = CaptchaField(required=True)
