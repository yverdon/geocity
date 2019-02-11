# Create your models here.
from django.contrib.gis.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from  django.core.validators import RegexValidator

class Actor(models.Model):

    name = models.CharField(_("name"), max_length=100, null=True)
    firstname = models.CharField(_("firstname"), max_length=100, null=True)
    company_name = models.CharField(_("company_name"), max_length=100, null=True)
    vat_number = models.CharField(_("vat_number"),
        max_length=100,
        null=True,
        validators=[
            RegexValidator(
                regex='([CHE-])+\d{3}[.]+\d{3}[.]+\d{3}',
                message='Le code d\'entreprise doit être de type CHE-123.456.789 et vous pouvez le trouver sur \
                le registe fédéral des entreprises \
                https://www.uid.admin.ch/search.aspx'
        )])
    address = models.CharField(_("address"), max_length=100, null=True)
    zipcode = models.PositiveIntegerField(_("zipcode"), null=True)
    city = models.CharField(_("city"), max_length=100, null=True)
    phone_fixed = models.CharField(_("phone_fixed"),
        null=True,
        max_length=20,
        validators=[
            RegexValidator(
                regex='^(\s*[0-9]+\s*)+$',
                message='Seuls les chiffres et les espaces sont autorisés'
        )])
    phone_mobile = models.CharField(_("phone_mobile"),
        null=True,
        blank=True,
        max_length=20,
        validators=[
            RegexValidator(
                regex='^(\s*[0-9]+\s*)+$',
                message='Seuls les chiffres et les espaces sont autorisés'
        )])
    email = models.EmailField(_("email"), null=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('actor')

    def __str__(self):
        return self.name


class Department(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    description = models.CharField(_('description'), max_length=100, default='Service')
    is_validator = models.BooleanField(_("is_validator"))
    is_admin = models.BooleanField(_("is_admin"))
    is_archeologist = models.BooleanField(_("is_archeologist"))

    class Meta:
        verbose_name = _('department')

    def __str__(self):
        return str(self.group)


class SiteType(models.Model):

    description = models.CharField(_('description'), max_length=100)

    class Meta:
        verbose_name = _('sitetype')

    def __str__(self):
        return self.description


class CreditorType(models.Model):
    name = models.CharField(_("creditor_name"), max_length=100)
    class Meta:
        verbose_name = _('creditortype')

    def __str__(self):
        return self.name

class PermitRequest(models.Model):
    amount = models.PositiveIntegerField(_("amount"),null=True, blank=True)
    paid = models.BooleanField(_("payed"),default=False)
    validated = models.BooleanField(_("is_valid"), default=False)
    sent = models.BooleanField(_("sent"), default=False)
    ended = models.BooleanField(_("ended"), default=False)
    date_start = models.DateField(_("date_start"))
    date_end = models.DateField(_("date_end"))
    date_effective_end = models.DateField(_("date_effective_end"), null=True, blank=True)
    length = models.DecimalField(_("length"), max_digits=7, decimal_places=2)
    width = models.DecimalField(_("with"), max_digits=7, decimal_places=2)
    road_marking_damaged = models.BooleanField(_("road_marking_damaged"))
    is_green_area = models.BooleanField(_("is_green_area"))
    invoice_to = models.ForeignKey(CreditorType, on_delete=models.SET_NULL, null=True, verbose_name=_("invoice_to"))
    company = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True, related_name='%(class)s_company', verbose_name=_("company"))
    project_owner = models.ForeignKey(Actor, on_delete=models.SET_NULL, null=True, related_name='%(class)s_project_owner', verbose_name=_("project_owner"))
    sitetype = models.ForeignKey(SiteType, on_delete=models.SET_NULL, null=True, verbose_name=_("sitetype"))
    description = models.TextField(_("description"))
    has_archeology = models.BooleanField(_("has_archeology"), default=False)
    has_existing_archeology = models.BooleanField(_("has_existing_archeology"), default=False)
    address = models.CharField(_("address"), max_length=100, null=True)
    zipcode = models.PositiveIntegerField(_("zipcode"), null=True)
    city = models.CharField(_("city"), max_length=100, null=True)
    date_end_work = models.DateField(_("date_end_work"),null=True, blank=True)
    date_end_work_announcement = models.DateField(_("date_end_work_announcement"),null=True, blank=True)
    date_last_printed = models.DateField(_("date_last_printed"),null=True, blank=True)
    report_filename = models.CharField(_("report_filename"), max_length=254, null=True)
    date_request_created = models.DateField(_("date_request_created"),null=True)
    geom = models.MultiPointField(_("geom"), srid=2056)

    class Meta:
        verbose_name = _('permitrequest')
        permissions = (
            ("change_amount", "Can change amount"),
            ("change_paid", "Can change paid"),
            ("change_geom", "Can change geom"),
            ("change_validated", "Can change validated"),
            ("change_sent", "Can change sent"),
            ("change_ended", "Can change ended"),
            ("change_date_effective_end", "Can change date_effective_end"),
            ("change_has_existing_archeology", "Can change has_existing_archeology")
         )

    def __str__(self):
        return 'Permit ' + str(self.id)


class Validation(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    permitrequest = models.ForeignKey(PermitRequest, on_delete=models.CASCADE)
    accepted = models.BooleanField(_("accepted"))
    comment = models.TextField(_("comment"), null=True, blank=True)

    class Meta:
        verbose_name = _('validation')

    def __str__(self):
        return str(self.department) + '-' + str(self.permitrequest)

class Document(models.Model):

    permitrequest = models.ForeignKey(PermitRequest, on_delete=models.CASCADE)
    file_path = models.CharField(_("file_path"), max_length=1024)
    file_name = models.CharField(_("file_name"), max_length=512, null=True)

    class Meta:
        verbose_name = _('document')

    def __str__(self):
        return self.file_path

class Mail(models.Model):

    type = models.CharField(_("mail_type"), max_length=128, unique=True)
    recipients = models.CharField(_("recipients"), max_length=1024)
    subject = models.CharField(_("subject"), max_length=128)
    body = models.TextField(_("body"))

    class Meta:
        verbose_name = _('mail')

    def __str__(self):
        return 'Mail' + str(self.id)

class Archelogy(models.Model):
    fiche = models.TextField(_("fiche"),null=True)
    commune = models.TextField(_("commune"),null=True)
    descriptio = models.TextField(_("descriptio"),null=True)
    note_carto = models.TextField(_("note_carto"),null=True)
    annee_revi = models.TextField(_("annee_revi"),null=True)
    id_per = models.TextField(_("id_per"),null=True)
    lien_img = models.TextField(_("lien_img"),null=True)
    note_detai = models.TextField(_("note_detai"),null=True)
    shape_len = models.TextField(_("shape_len"),null=True)
    date_maj = models.TextField(_("date_maj"),null=True)
    guid = models.TextField(_("guid"),null=True)
    mention = models.TextField(_("mention"),null=True)
    fme_feat = models.TextField(_("fme_feat"),null=True)
    autre_ment = models.TextField(_("autre_ment"),null=True)
    multi_read = models.TextField(_("multi_read"),null=True)
    autre_mesu = models.TextField(_("autre_mesu"),null=True)
    shape_area = models.TextField(_("shape_area"),null=True)
    objectid = models.TextField(_("objectid"),null=True)
    date_mesur = models.TextField(_("date_mesur"),null=True)
    eca = models.TextField(_("eca"),null=True)
    url_recens = models.TextField(_("url_recens"),null=True)
    mesure = models.TextField(_("mesure"),null=True)
    import_date = models.PositiveIntegerField(_("import_date"),null=True)
    geom = models.MultiPolygonField(_("geom"),srid=2056)

    class Meta:
        verbose_name = _('archelogy')

    def __str__(self):
        return 'Archelogy' + str(self.id)
