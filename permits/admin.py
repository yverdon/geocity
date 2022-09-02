import django.db.models
from adminsortable2.admin import SortableAdminMixin
from django import forms
from django.contrib import admin, messages
from django.contrib.admin import AdminSite, site
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import Group, Permission, User
from django.core.management import CommandError, call_command
from django.db.models import Q, Value
from django.db.models.functions import StrIndex, Substr
from django.http import Http404
from django.shortcuts import redirect
from django.urls import re_path, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from geomapshark import permissions_groups, settings

from . import forms as permit_forms
from . import models

MULTIPLE_INTEGRATOR_ERROR_MESSAGE = "Un utilisateur membre d'un groupe de type 'Intégrateur' ne peut être que dans un et uniquement un groupe 'Intégrateur'"

PERMIT_DURATION_ERROR_MESSAGE = "Veuillez saisir une valeur > 0"
DAYS_BEFORE_REMINDER_ERROR_MESSAGE = (
    "Si la fonction de rappel est active, il faut saisir une valeur de délai valide"
)

# Allow a user belonging to integrator group to see only objects created by this group
def filter_for_user(user, qs):
    if not user.is_superuser:
        qs = qs.filter(
            integrator__in=user.groups.filter(
                permitdepartment__is_integrator_admin=True
            )
        )
    return qs


def get_integrator_readonly_fields(user):
    if user.is_superuser:
        return []
    else:
        return ["integrator"]


class PermitsAdminSite(AdminSite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._registry.update(site._registry)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            re_path(
                r"^create-anonymous-user/$",
                self.create_anonymous_user,
                name="create_anonymous_user",
            ),
            re_path(
                r"^create-knox-token/$",
                self.create_knox_token,
                name="create_knox_token",
            ),
        ]
        return custom_urls + urls

    @method_decorator(staff_member_required)
    @method_decorator(require_POST)
    def create_anonymous_user(self, request):
        """
        Admin custom view to create the anonymous user for the given Administrative
        entity.
        FIXME: Special permission required to do that ?
         Like being an integrator of the given entity ?
        """
        try:
            entity_id = int(request.POST.get("entity_id"))
        except ValueError:
            raise Http404

        try:
            call_command("create_anonymous_users", entity_id)
        except CommandError:
            # Display error
            messages.add_message(
                request,
                messages.ERROR,
                _("Echec de la création de l'utilisateur anonyme."),
            )
        else:
            messages.add_message(
                request, messages.SUCCESS, _("Utilisateur anonyme créé avec succès.")
            )

        return redirect(
            reverse(
                "admin:permits_permitadministrativeentity_change",
                kwargs={"object_id": entity_id},
            )
        )

    @method_decorator(staff_member_required)
    @method_decorator(require_POST)
    def create_knox_token(self, request):
        """
        Admin custom view to create the knox token for the given User
        """
        user_id = int(request.POST.get("user"))
        request_user_id = request.user.id
        try:
            token = call_command("create_knox_token", user_id, request_user_id)
        except CommandError:
            # Display error
            messages.add_message(
                request,
                messages.ERROR,
                _("Echec de la création du knox token."),
            )
        else:
            messages.add_message(
                request,
                messages.SUCCESS,
                _(
                    "Knox token créé avec succès. Veuillez le copier, il ne sera visible qu'une seule fois."
                ),
            )
            messages.add_message(request, messages.INFO, token)

        return redirect(
            reverse(
                "admin:auth_user_change",
                kwargs={"object_id": user_id},
            )
        )


class IntegratorFilterMixin:
    def save_model(self, request, obj, form, change):
        user = request.user
        if not user.is_superuser:
            obj.integrator = user.groups.get(permitdepartment__is_integrator_admin=True)
        super().save_model(request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        user = request.user
        return get_integrator_readonly_fields(user)

    def get_queryset(self, request):
        user = request.user
        return filter_for_user(user, super().get_queryset(request))


class UserAdminForm(UserChangeForm):
    def clean_groups(self):
        groups = self.cleaned_data["groups"]

        edited_user_integrator_groups = groups.filter(
            permitdepartment__is_integrator_admin=True
        )

        if len(edited_user_integrator_groups) > 1:
            raise forms.ValidationError(MULTIPLE_INTEGRATOR_ERROR_MESSAGE)
        return groups


class UserAdmin(BaseUserAdmin):
    form = UserAdminForm
    fieldsets = (
        (
            None,
            {"fields": ("username",)},
        ),
        (
            "Informations personnelles",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "is_sociallogin",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Dates importantes",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "is_sociallogin",
        "last_login",
        "date_joined",
    )

    def has_add_permission(self, request):
        return False

    @admin.display(boolean=True)
    def is_sociallogin(self, obj):
        return obj.socialaccount_set.exists()

    is_sociallogin.admin_order_field = "socialaccount"
    is_sociallogin.short_description = "Social"

    change_form_template = "permits/admin/user_change.html"

    def get_readonly_fields(self, request, obj=None):
        # limit editable fields to protect user data, superuser creation must be done using django shell
        if request.user.is_superuser:
            return [
                "is_superuser",
                "is_sociallogin",
            ]
        else:
            return [
                "email",
                "username",
                "user_permissions",
                "is_superuser",
                "is_sociallogin",
                "is_staff",
                "last_login",
                "date_joined",
            ]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        user_being_updated = User.objects.get(
            id=(int(request.resolver_match.kwargs["object_id"]))
        )
        integrator_group_for_user_being_updated = user_being_updated.groups.filter(
            permitdepartment__is_integrator_admin=True
        )
        if db_field.name == "groups":
            if request.user.is_superuser:
                kwargs["queryset"] = Group.objects.all()
            else:
                kwargs["queryset"] = Group.objects.filter(
                    permitdepartment__integrator=request.user.groups.get(
                        permitdepartment__is_integrator_admin=True
                    ).pk,
                )

                if integrator_group_for_user_being_updated:
                    kwargs["queryset"] = (
                        kwargs["queryset"] | integrator_group_for_user_being_updated
                    ).distinct()

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # Only superuser can edit superuser users
    def get_queryset(self, request):
        # Only allow integrator to change users that have no group, are not superuser or are in group administrated by integrator.
        if request.user.is_superuser:
            qs = User.objects.all()
        else:
            user_integrator_group = request.user.groups.get(
                permitdepartment__is_integrator_admin=True
            )
            qs = (
                User.objects.filter(
                    Q(is_superuser=False),
                    Q(groups__permitdepartment__integrator=user_integrator_group.pk)
                    | Q(groups__isnull=True),
                )
                .annotate(
                    email_domain=Substr("email", StrIndex("email", Value("@")) + 1)
                )
                .distinct()
            )

            qs = qs.filter(
                Q(
                    email_domain__in=user_integrator_group.permitdepartment.integrator_email_domains.split(
                        ","
                    )
                )
                | Q(
                    email__in=user_integrator_group.permitdepartment.integrator_emails_exceptions.split(
                        ","
                    )
                )
            )

        return qs

    def save_model(self, req, obj, form, change):
        """Set 'is_staff=True' when the saved user is in a integrator group.
        But let is_staff=True for super users.
        """
        if req.user.is_superuser:
            obj.is_staff = False if not obj.is_superuser else True
            for group in form.cleaned_data["groups"]:
                if group.permitdepartment.is_integrator_admin:
                    obj.is_staff = True

        super().save_model(req, obj, form, change)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class DepartmentAdminForm(forms.ModelForm):
    class Meta:
        model = models.PermitDepartment
        fields = [
            "description",
            "administrative_entity",
            "is_validator",
            "is_default_validator",
            "is_backoffice",
            "is_integrator_admin",
            "mandatory_2fa",
            "integrator_email_domains",
            "integrator_emails_exceptions",
            "integrator",
        ]

    # If the group is updated to be integrator, the users in this group should not be in another integrator group
    # If the group is updated to be integrator, the administrative_entity will be None. The integrator will create entities, so they don't exist yet
    def clean(self):
        group = self.cleaned_data["group"]

        # Integrator users don't have the field "is_integrator_admin" while creating a group
        if "is_integrator_admin" in self.cleaned_data:
            is_integrator_admin = self.cleaned_data["is_integrator_admin"]
        else:
            is_integrator_admin = False

        # Check only if the group passed from not integrator to integrator and has a user_set
        try:
            if (
                self.instance
                and not self.instance.is_integrator_admin
                and is_integrator_admin
                and group.user_set
            ):
                user_with_integrator_group = (
                    Group.objects.exclude(pk=group.pk)
                    .filter(
                        user__in=group.user_set.all(),
                        permitdepartment__is_integrator_admin=True,
                    )
                    .exists()
                )
                # Raise error if this group is integrator and user(s) is/are already in integrator group and this group
                if user_with_integrator_group:
                    raise forms.ValidationError(
                        {"is_integrator_admin": MULTIPLE_INTEGRATOR_ERROR_MESSAGE}
                    )
        except ValueError:
            # Upon creation of the group, there is no id, therefore no user_set
            pass

        # Raise error if group is not integrator and has no administrative_entity
        if (
            not is_integrator_admin
            and self.instance.is_integrator_admin
            and not self.cleaned_data["administrative_entity"]
        ):
            raise forms.ValidationError(
                {
                    "administrative_entity": _(
                        "Un groupe non intégrateur doit avoir une entité administrative"
                    )
                }
            )

        return self.cleaned_data


# Inline for group & department (1to1)
class PermitDepartmentInline(admin.StackedInline):
    model = models.PermitDepartment
    can_delete = False
    verbose_name_plural = "Service"
    inline_classes = ("collapse open",)
    form = DepartmentAdminForm
    min_num = 1

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "administrative_entity":
            if request.user.is_superuser:
                kwargs["queryset"] = models.PermitAdministrativeEntity.objects.all()
            else:
                kwargs["queryset"] = models.PermitAdministrativeEntity.objects.filter(
                    integrator=request.user.groups.get(
                        permitdepartment__is_integrator_admin=True
                    )
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return []
        else:
            return [
                "integrator",
                "is_integrator_admin",
                "integrator_email_domains",
                "integrator_emails_exceptions",
            ]


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        help_texts = {
            "permissions": _(
                "Pour un rôle intégrateur, ajoutez toutes les permissions disponibles"
            ),
        }

    def clean_permissions(self):
        permissions = self.cleaned_data["permissions"]
        integrator_permissions = Permission.objects.filter(
            (
                (
                    Q(content_type__app_label="permits")
                    & Q(
                        content_type__model__in=permissions_groups.INTEGRATOR_PERMITS_MODELS_PERMISSIONS
                    )
                )
                | (
                    Q(content_type__app_label="reports")
                    & Q(
                        content_type__model__in=permissions_groups.INTEGRATOR_REPORTS_MODELS_PERMISSIONS
                    )
                )
            )
            | Q(codename__in=permissions_groups.OTHER_PERMISSIONS_CODENAMES)
        )

        if "permitdepartment-0-is_integrator_admin" in self.data.keys():
            permissions = permissions.union(integrator_permissions)
        else:
            permissions = permissions.difference(
                integrator_permissions.exclude(
                    codename__in=permissions_groups.AVAILABLE_FOR_INTEGRATOR_PERMISSION_CODENAMES
                )
            )
        return permissions


class GroupAdmin(admin.ModelAdmin):
    inlines = (PermitDepartmentInline,)
    form = GroupAdminForm
    list_display = [
        "__str__",
        "get__integrator",
        "get__is_validator",
        "get__is_default_validator",
        "get__is_backoffice",
        "get__mandatory_2fa",
    ]

    filter_horizontal = ("permissions",)
    search_fields = [
        "name",
    ]

    @admin.display(boolean=True)
    def get__is_validator(self, obj):
        return obj.permitdepartment.is_validator

    get__is_validator.admin_order_field = "permitdepartment__is_validator"
    get__is_validator.short_description = _("Validateur")

    @admin.display(boolean=True)
    def get__is_default_validator(self, obj):
        return obj.permitdepartment.is_default_validator

    get__is_default_validator.admin_order_field = (
        "permitdepartment__is_default_validator"
    )
    get__is_default_validator.short_description = _("Validateur par défaut")

    @admin.display(boolean=True)
    def get__is_backoffice(self, obj):
        return obj.permitdepartment.is_backoffice

    get__is_backoffice.admin_order_field = "permitdepartment__is_backoffice"
    get__is_backoffice.short_description = _("Secrétariat")

    def get__integrator(self, obj):
        return Group.objects.get(pk=obj.permitdepartment.integrator)

    get__integrator.admin_order_field = "permitdepartment__integrator"
    get__integrator.short_description = _("Groupe des administrateurs")

    @admin.display(boolean=True)
    def get__mandatory_2fa(self, obj):
        return obj.permitdepartment.mandatory_2fa

    get__mandatory_2fa.admin_order_field = "permitdepartment__mandatory_2fa"
    get__mandatory_2fa.short_description = _("2FA obligatoire")

    def get_queryset(self, request):

        if request.user.is_superuser:
            qs = Group.objects.all()
        else:
            qs = Group.objects.filter(
                Q(
                    permitdepartment__integrator=request.user.groups.get(
                        permitdepartment__is_integrator_admin=True
                    ).pk
                )
            )
        return qs

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.permitdepartment.integrator = request.user.groups.get(
                permitdepartment__is_integrator_admin=True
            ).pk
        super().save_model(request, obj, form, change)
        obj.permitdepartment.save()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # permissions that integrator role can grant to group
        if db_field.name == "permissions":

            if (
                not request.user.is_superuser
                and request.user.groups.get(
                    permitdepartment__is_integrator_admin=True
                ).pk
            ):
                integrator_permissions = Permission.objects.filter(
                    codename__in=permissions_groups.AVAILABLE_FOR_INTEGRATOR_PERMISSION_CODENAMES
                )
                kwargs["queryset"] = integrator_permissions

        return super().formfield_for_manytomany(db_field, request, **kwargs)


admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)


def works_object_type_administrative_entities(obj):
    return ", ".join(
        administrative_entity.name
        for administrative_entity in obj.administrative_entities.all()
    )


def get_works_object_types_field(user):

    qs = (
        models.WorksObjectType.objects.select_related("works_object", "works_type")
        .order_by("works_object__name", "works_type__name")
        .prefetch_related("administrative_entities")
    )

    if not user.is_superuser:
        qs = qs.filter(
            integrator__in=user.groups.filter(
                permitdepartment__is_integrator_admin=True
            )
        )

    return WorksObjectTypeWithAdministrativeEntitiesField(
        queryset=qs,
        widget=forms.CheckboxSelectMultiple,
        label=_("objets").capitalize(),
    )


works_object_type_administrative_entities.short_description = _(
    "Entités administratives"
)


class WorksObjectTypeAdminForm(forms.ModelForm):
    class GeometryTypes(django.db.models.TextChoices):
        POINT = "has_geometry_point", _("Point")
        LINE = "has_geometry_line", _("Ligne")
        POLYGON = "has_geometry_polygon", _("Polygone")

    geometry_types = forms.MultipleChoiceField(
        choices=GeometryTypes.choices,
        widget=forms.CheckboxSelectMultiple,
        label=_("Types de géométrie autorisés"),
        required=False,
    )

    class Meta:
        model = models.WorksObjectType
        fields = "__all__"
        widgets = {
            "is_public": forms.RadioSelect(
                choices=models.PUBLIC_TYPE_CHOICES,
            ),
        }

    class Media:
        js = ("js/admin/works_object_type.js",)

    def __init__(self, *args, **kwargs):
        instance = kwargs.get("instance")
        if instance:
            kwargs["initial"] = dict(
                geometry_types=[
                    geometry_type
                    for geometry_type in self.GeometryTypes.values
                    if getattr(instance, geometry_type)
                ],
                **kwargs.get("initial", {}),
            )

        super().__init__(*args, **kwargs)

    def clean_days_before_reminder(self):
        if (
            self.cleaned_data["expiration_reminder"]
            and self.cleaned_data["days_before_reminder"] is None
        ):
            raise forms.ValidationError(DAYS_BEFORE_REMINDER_ERROR_MESSAGE)
        return self.cleaned_data["days_before_reminder"]

    def clean_permit_duration(self):
        if self.cleaned_data["permit_duration"]:
            if self.cleaned_data["permit_duration"] <= 0:
                raise forms.ValidationError(PERMIT_DURATION_ERROR_MESSAGE)
        return self.cleaned_data["permit_duration"]

    def save(self, *args, **kwargs):
        for geometry_type in self.GeometryTypes.values:
            setattr(
                self.instance,
                geometry_type,
                geometry_type in self.cleaned_data["geometry_types"],
            )

        return super().save(*args, **kwargs)


class WorksObjectTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = WorksObjectTypeAdminForm
    list_display = [
        "sortable_str",
        works_object_type_administrative_entities,
        "can_always_update",
        "is_public",
        "requires_payment",
        "requires_validation_document",
        "is_anonymous",
        "notify_services",
        "needs_date",
        "permit_duration",
        "expiration_reminder",
        "days_before_reminder",
        "has_geometry_point",
        "has_geometry_line",
        "has_geometry_polygon",
        "document_enabled",
        "publication_enabled",
        "permanent_publication_enabled",
    ]
    list_filter = ["administrative_entities"]
    search_fields = [
        "works_type__name",
        "works_object__name",
        "administrative_entities__name",
    ]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "works_type",
                    "works_object",
                    "administrative_entities",
                    "can_always_update",
                    "is_public",
                    "requires_payment",
                    "requires_validation_document",
                    "is_anonymous",
                    "integrator",
                )
            },
        ),
        (
            "Notifications aux services",
            {"fields": ("notify_services", "services_to_notify")},
        ),
        (
            "Planning et localisation",
            {
                "fields": (
                    "can_have_multiple_ranges",
                    "geometry_types",
                    "needs_date",
                    "start_delay",
                )
            },
        ),
        (
            "Modules complémentaires",
            {
                "fields": (
                    "document_enabled",
                    "publication_enabled",
                    "permanent_publication_enabled",
                )
            },
        ),
        (
            "Prolongation",
            {
                "fields": (
                    "permit_duration",
                    "expiration_reminder",
                    "days_before_reminder",
                )
            },
        ),
        (
            "Directive",
            {
                "fields": (
                    "directive",
                    "directive_description",
                    "additional_information",
                )
            },
        ),
    )

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "works_object__name"
    sortable_str.short_description = _("1.4 Configuration du type-objet-entité")

    def get_queryset(self, request):
        qs = (
            super()
            .get_queryset(request)
            .select_related("works_object", "works_type")
            .prefetch_related("administrative_entities")
        )
        return qs

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "administrative_entities":
            if request.user.is_superuser:
                kwargs["queryset"] = models.PermitAdministrativeEntity.objects.all()
            else:
                kwargs["queryset"] = models.PermitAdministrativeEntity.objects.filter(
                    integrator=request.user.groups.get(
                        permitdepartment__is_integrator_admin=True
                    )
                )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        user = request.user

        if db_field.name == "works_type":
            qs = models.WorksType.objects.all()
            kwargs["queryset"] = filter_for_user(user, qs)

        if db_field.name == "works_object":
            qs = models.WorksObject.objects.all()
            kwargs["queryset"] = filter_for_user(user, qs)

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class WorksObjectTypeWithAdministrativeEntitiesField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        entities = ", ".join(
            entity.name for entity in obj.administrative_entities.all()
        )
        return f"{obj.works_object} ({obj.works_type}) - {entities}"


class WorksObjectPropertyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["works_object_types"] = get_works_object_types_field(user)

    class Meta:
        model = models.WorksObjectProperty
        fields = [
            "name",
            "placeholder",
            "help_text",
            "order",
            "input_type",
            "services_to_notify",
            "choices",
            "line_number_for_textarea",
            "regex_pattern",
            "file_download",
            "is_mandatory",
            "is_public_when_permitrequest_is_public",
            "additional_searchtext_for_address_field",
            "store_geometry_for_address_field",
            "works_object_types",
            "integrator",
        ]

    def clean_file_download(self):
        if self.cleaned_data["input_type"] == "file_download":
            if not self.cleaned_data["file_download"]:
                raise forms.ValidationError(_("This field is required."))
        return self.cleaned_data["file_download"]

    class Media:
        js = ("js/admin/works_object_property.js",)


class WorksObjectPropertyAdmin(
    IntegratorFilterMixin, SortableAdminMixin, admin.ModelAdmin
):
    form = WorksObjectPropertyForm
    list_display = [
        "sortable_str",
        "is_mandatory",
        "is_public_when_permitrequest_is_public",
        "name",
        "input_type",
        "placeholder",
        "help_text",
    ]
    list_filter = [
        "name",
        "input_type",
        "works_object_types",
    ]
    search_fields = [
        "name",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("1.5 Configuration du champ")

    # Pass the request from ModelAdmin to ModelForm
    def get_form(self, request, obj=None, **kwargs):
        Form = super(WorksObjectPropertyAdmin, self).get_form(request, obj, **kwargs)

        class RequestForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs["user"] = request.user
                return Form(*args, **kwargs)

        return RequestForm


class SiteWithAdministrativeEntitiesField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.name} ({obj.domain})"


def get_sites_field(user):
    qs = models.Site.objects.all()
    if not user.is_superuser:
        qs = qs.filter(
            Q(
                integrator__in=user.groups.filter(
                    permitdepartment__is_integrator_admin=True
                )
            )
            | Q(domain=settings.DEFAULT_SITE)
        )

    return SiteWithAdministrativeEntitiesField(
        queryset=qs,
        widget=forms.CheckboxSelectMultiple,
        label=_("Sites").capitalize(),
    )


class PermitAdministrativeEntityAdminForm(forms.ModelForm):
    """Form class to configure an administrative entity (commune, organisation)"""

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["sites"] = get_sites_field(user)

    class Meta:
        model = models.PermitAdministrativeEntity
        fields = [
            "name",
            "tags",
            "ofs_id",
            "sites",
            "expeditor_email",
            "expeditor_name",
            "custom_signature",
            "link",
            "archive_link",
            "general_informations",
            "phone",
            "additional_searchtext_for_address_field",
            "geom",
            "integrator",
        ]
        exclude = ["enabled_status"]
        widgets = {
            "geom": permit_forms.GeometryWidget(
                attrs={
                    "options": {
                        "map_width": "100%",
                        "map_height": 400,
                        "default_center": [2539057, 1181111],
                        "default_zoom": 10,
                        "display_raw": False,
                        "edit_geom": True,
                        "min_zoom": 5,
                        "wmts_capabilities_url": settings.WMTS_GETCAP,
                        "wmts_layer": settings.WMTS_LAYER,
                        "wmts_capabilities_url_alternative": settings.WMTS_GETCAP_ALTERNATIVE,
                        "wmts_layer_alternative": settings.WMTS_LAYER_ALTERNATIVE,
                        "restriction_area_enabled": False,
                        "geometry_db_type": "MultiPolygon",
                        "wms_layers": [],
                    },
                }
            ),
            "is_public": forms.RadioSelect(
                choices=models.PUBLIC_TYPE_CHOICES,
            ),
        }

    class Media:
        js = ("https://code.jquery.com/jquery-3.5.1.slim.min.js",)
        css = {
            "all": (
                "https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css",
                "css/admin.css",
            )
        }


class PermitWorkflowStatusInline(admin.StackedInline):
    model = models.PermitWorkflowStatus
    extra = 0
    verbose_name = _("Étape - ")
    verbose_name_plural = _(
        "Étapes - Si aucune n'est ajoutée manuellement, toutes les étapes sont ajoutées automatiquement"
    )


class WorksObjectAdminForm(forms.ModelForm):
    class Meta:
        model = models.WorksObject
        fields = [
            "name",
            "wms_layers",
            "wms_layers_order",
            "integrator",
        ]
        widgets = {
            "wms_layers": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "ex: https://mywmserver.ch?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&"
                    + "FORMAT=image%2Fpng&TRANSPARENT=true&LAYERS=my_layer_name&SERVERTYPE="
                    + "mapserver&CRS=EPSG%3A2056",
                }
            ),
        }
        help_texts = {
            "wms_layers": "URL pour la ou les couches WMS utiles à la saisie de la demande pour ce type d'objet",
            "wms_layers_order": "Ordre de(s) la(les) couche(s) dans la carte. 1: au-dessus",
        }


class WorksObjectAdmin(IntegratorFilterMixin, SortableAdminMixin, admin.ModelAdmin):
    form = WorksObjectAdminForm
    list_filter = [
        "name",
    ]
    search_fields = [
        "name",
    ]
    list_display = [
        "sortable_str",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("1.3 Configuration de l'objet")


class PermitAdministrativeEntityAdmin(IntegratorFilterMixin, admin.ModelAdmin):

    # Pass the request from ModelAdmin to ModelForm
    def get_form(self, request, obj=None, **kwargs):
        Form = super(PermitAdministrativeEntityAdmin, self).get_form(
            request, obj, **kwargs
        )

        class RequestForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs["user"] = request.user
                return Form(*args, **kwargs)

        return RequestForm

    change_form_template = "permits/admin/permit_administrative_entity_change.html"
    form = PermitAdministrativeEntityAdminForm
    inlines = [
        PermitWorkflowStatusInline,
    ]
    list_filter = [
        "name",
    ]
    search_fields = [
        "name",
    ]
    list_display = [
        "sortable_str",
        "expeditor_name",
        "expeditor_email",
        "ofs_id",
        "get_tags",
        "get_sites",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = (
        "1.1 Configuration de l'entité administrative (commune, organisation)"
    )

    def get_sites(self, obj):
        return [site["name"] for site in obj.sites.all().values("name")]

    get_sites.short_description = _("Sites")
    get_sites.admin_order_field = "sites__name"

    def get_tags(self, obj):
        return [tag["name"] for tag in obj.tags.all().values("name")]

    get_tags.short_description = _("Mots-clés")
    get_tags.admin_order_field = "tags__name"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):

        if db_field.name == "integrator":
            kwargs["queryset"] = Group.objects.filter(
                permitdepartment__is_integrator_admin=True,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):

        if not request.user.is_superuser:
            obj.integrator = request.user.groups.get(
                permitdepartment__is_integrator_admin=True
            )
        obj.save()
        has_workflow_status = models.PermitWorkflowStatus.objects.filter(
            administrative_entity=obj
        ).exists()
        if not has_workflow_status:
            for key, value in models.PermitRequest.STATUS_CHOICES:
                models.PermitWorkflowStatus.objects.create(
                    status=key,
                    administrative_entity=obj,
                )


class PermitRequestAmendPropertyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["works_object_types"] = get_works_object_types_field(user)

    class Meta:
        model = models.PermitRequestAmendProperty
        fields = [
            "name",
            "is_mandatory",
            "is_visible_by_author",
            "can_always_update",
            "works_object_types",
            "integrator",
        ]


class PermitRequestAmendPropertyAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    list_display = [
        "sortable_str",
        "is_mandatory",
        "is_visible_by_author",
        "can_always_update",
    ]
    search_fields = [
        "name",
    ]
    form = PermitRequestAmendPropertyForm

    def sortable_str(self, obj):
        return str(obj)

    sortable_str.short_description = (
        "2.2 Configuration du champ de traitement des demandes"
    )
    sortable_str.admin_order_field = "name"

    # Pass the request from ModelAdmin to ModelForm
    def get_form(self, request, obj=None, **kwargs):
        Form = super(PermitRequestAmendPropertyAdmin, self).get_form(
            request, obj, **kwargs
        )

        class RequestForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs["user"] = request.user
                return Form(*args, **kwargs)

        return RequestForm


class PermitActorTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    list_display = [
        "sortable_str",
        "type",
        "works_type",
        "is_mandatory",
    ]
    list_filter = [
        "works_type",
        "is_mandatory",
    ]
    search_fields = [
        "name",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "type"
    sortable_str.short_description = _("1.6 Configuration du contact")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "works_type":
            kwargs["queryset"] = filter_for_user(
                request.user, models.WorksType.objects.all()
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class WorksTypeAdminForm(forms.ModelForm):
    class Meta:
        model = models.WorksType
        fields = [
            "name",
            "meta_type",
            "tags",
            "integrator",
        ]


class WorksTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = WorksTypeAdminForm
    list_display = [
        "sortable_str",
        "meta_type",
        "get__tags",
    ]
    search_fields = [
        "id",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("1.2 Configuration du type")

    def get__tags(self, obj):
        return list(obj.tags.all())

    get__tags.short_description = _("Mots-clés")


class PermitRequestAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "created_at",
        "status",
        "author",
        "get_works_object_types",
        "administrative_entity",
    ]
    search_fields = [
        "id",
        "author__user__first_name",
        "author__user__last_name",
    ]
    list_filter = ("status", "author", "works_object_types", "administrative_entity")

    def has_add_permission(self, request):
        return False

    def get_works_object_types(self, obj):
        return ", ".join(
            sorted([wot.__str__() for wot in obj.works_object_types.all()])
        )

    get_works_object_types.admin_order_field = "works_object_types"
    get_works_object_types.short_description = "Objets et types de demandes"


class TemplateCustomizationAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "templatename",
        "application_title",
        "application_subtitle",
        "has_background_image",
    ]
    list_filter = [
        "templatename",
        "application_title",
    ]
    search_fields = [
        "templatename",
    ]

    @admin.display(boolean=True)
    def has_background_image(self, obj):
        try:
            return obj.background_image.url is not None
        except ValueError:
            return False

    has_background_image.admin_order_field = "background_image"
    has_background_image.short_description = "Image de fond"


class ComplementaryDocumentTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = permit_forms.ComplementaryDocumentTypeAdminForm

    fields = ["name", "parent", "work_object_types", "integrator"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "work_object_types":
            if request.user.is_superuser:
                kwargs["queryset"] = models.WorksObjectType.objects.all()
            else:
                kwargs["queryset"] = models.WorksObjectType.objects.filter(
                    integrator=request.user.groups.get(
                        permitdepartment__is_integrator_admin=True
                    )
                )
        if db_field.name == "parent":
            if request.user.is_superuser:
                kwargs["queryset"] = models.ComplementaryDocumentType.objects.all()
            else:
                kwargs["queryset"] = models.ComplementaryDocumentType.objects.filter(
                    integrator=request.user.groups.get(
                        permitdepartment__is_integrator_admin=True
                    )
                )

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PermitRequestInquiryAdmin(admin.ModelAdmin):
    list_display = ("id", "start_date", "end_date", "submitter", "permit_request")

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("3.2 Enquêtes public")


class SiteProfileAdminForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = "__all__"


class SiteProfileAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = SiteProfileAdminForm
    list_display = [
        "integrator",
    ]

    def sortable_str(self, obj):
        return obj.__str__()

    sortable_str.admin_order_field = "name"
    sortable_str.short_description = _("15.0 Configuration des sites")


# admin.site.unregister(Site)
admin.site.register(models.Profile, SiteProfileAdmin)
admin.site.register(models.PermitActorType, PermitActorTypeAdmin)
admin.site.register(models.WorksType, WorksTypeAdmin)
admin.site.register(models.WorksObjectType, WorksObjectTypeAdmin)
admin.site.register(models.WorksObjectProperty, WorksObjectPropertyAdmin)
admin.site.register(models.PermitAdministrativeEntity, PermitAdministrativeEntityAdmin)
admin.site.register(models.WorksObject, WorksObjectAdmin)
admin.site.register(models.PermitRequestAmendProperty, PermitRequestAmendPropertyAdmin)
admin.site.register(models.TemplateCustomization, TemplateCustomizationAdmin)
admin.site.register(models.PermitRequest, PermitRequestAdmin)
admin.site.register(models.ComplementaryDocumentType, ComplementaryDocumentTypeAdmin)
admin.site.register(models.PermitRequestInquiry, PermitRequestInquiryAdmin)
