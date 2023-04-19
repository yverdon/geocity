from allauth.socialaccount.forms import SignupForm
from allauth.socialaccount.providers.base import ProviderException
from captcha.fields import CaptchaField
from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from geocity.fields import AddressWidget

from . import models
from .dootix.adapter import DootixSocialAccountAdapter
from .dootix.provider import DootixProvider
from .geomapfish.adapter import GeomapfishSocialAccountAdapter
from .geomapfish.provider import GeomapfishProvider


def check_existing_email(email, user):
    if (
        models.User.objects.filter(email=email)
        .exclude(Q(id=user.id) if user else Q())
        .exists()
    ):
        raise forms.ValidationError(_("Cet email est déjà utilisé."))

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

        if not "username" in cleaned_data:
            raise forms.ValidationError({"username": ""})

        if not "first_name" in cleaned_data:
            raise forms.ValidationError({"first_name": ""})

        if not "last_name" in cleaned_data:
            raise forms.ValidationError({"last_name": ""})

        if not "email" in cleaned_data:
            raise forms.ValidationError({"email": ""})

        for reserved_usernames in (
            settings.TEMPORARY_USER_PREFIX,
            settings.ANONYMOUS_USER_PREFIX,
        ):
            if cleaned_data["username"].startswith(reserved_usernames):
                raise forms.ValidationError(
                    {
                        "username": _(
                            "Le nom d'utilisat·eur·rice ne peut pas commencer par %s"
                        )
                        % reserved_usernames
                    }
                )

        if cleaned_data["first_name"] == settings.ANONYMOUS_NAME:
            raise forms.ValidationError(
                {
                    "first_name": _("Le prénom ne peut pas être %s")
                    % settings.ANONYMOUS_NAME
                }
            )

        if cleaned_data["last_name"] == settings.ANONYMOUS_NAME:
            raise forms.ValidationError(
                {"last_name": _("Le nom ne peut pas être %s") % settings.ANONYMOUS_NAME}
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
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
            raise forms.ValidationError(
                _("Le prénom ne peut pas être %s") % settings.ANONYMOUS_NAME
            )
        else:
            return self.cleaned_data["first_name"]

    def clean_last_name(self):
        if self.cleaned_data["last_name"] == settings.ANONYMOUS_NAME:
            raise forms.ValidationError(
                _("Le nom ne peut pas être %s") % settings.ANONYMOUS_NAME
            )
        else:
            return self.cleaned_data["last_name"]

    class Meta:
        model = models.User
        fields = ["first_name", "last_name", "email"]


class GenericUserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        create = kwargs.pop("create")
        super().__init__(*args, **kwargs)
        if create:
            self.fields["notify_per_email"].disabled = True
        else:
            self.fields.pop("captcha")

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
    captcha = CaptchaField(required=True)

    class Meta:
        model = models.UserProfile
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

        if settings.AUTHOR_IBAN_VISIBLE:
            fields.insert(7, "iban")

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
            "iban": forms.TextInput(
                attrs={"placeholder": "ex: CH12 3456 7890 1234 5678 9"}
            ),
            "company_name": forms.TextInput(
                attrs={"placeholder": "ex: Construction SA"}
            ),
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

    if settings.AUTHOR_IBAN_VISIBLE:
        iban = forms.CharField(
            required=False,
            label=_("IBAN"),
            max_length=30,
            widget=forms.TextInput(
                attrs={"placeholder": "ex: CH12 3456 7890 1234 5678 9"}
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
