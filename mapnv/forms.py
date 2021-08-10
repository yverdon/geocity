from allauth.socialaccount.adapter import get_adapter
from allauth.socialaccount.forms import SignupForm
from django import forms
from django.core.validators import RegexValidator

from permits.forms import AddressWidget
from django.utils.translation import gettext_lazy as _


class MapnvSocialSignupForm(SignupForm):
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
        super(MapnvSocialSignupForm, self).__init__(*args, **kwargs)
        self.fields["username"].label = _("Nom d’utilisateur")
        self.fields["username"].disabled = True
        self.fields["email"].disabled = True

    def save(self, request):
        adapter = get_adapter(request)
        return adapter.save_user(request, self.sociallogin, form=self)
