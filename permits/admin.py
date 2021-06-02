import django.db.models
from adminsortable2.admin import SortableAdminMixin
from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from geomapshark import settings
from django.db.models import Q
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import PermissionDenied
from django.forms import ValidationError
from django.contrib import messages
from django.contrib.auth.forms import UserChangeForm

from . import forms as permit_forms
from . import models

# define permissions required by integrator role
INTEGRATOR_PERMITS_MODELS_PERMISSIONS = [
    "permitadministrativeentity",
    "workstype",
    "worksobject",
    "worksobjecttype",
    "worksobjectproperty",
    "permitactortype",
    "permitrequestamendproperty",
    "permitdepartment",
    "permitworkflowstatus",
    "permitauthor",
]
OTHER_PERMISSIONS_CODENAMES = [
    "view_user",
    "change_user",
    "view_group",
    "add_group",
    "change_group",
    "delete_group",
    "see_private_requests",
]

MULTIPLE_INTEGRATOR_ERROR_MESSAGE = "Un utilisateur membre d'un groupe de type 'Intégrateur' ne peut être que dans un et uniquement un groupe 'Intégrateur'"

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
            raise forms.ValidationError(
                MULTIPLE_INTEGRATOR_ERROR_MESSAGE
            )
        return groups


class UserAdmin(BaseUserAdmin):
    form = UserAdminForm
    fieldsets = (
        (None, {"fields": ("username",)},),
        (
            "Informations personnelles",
            {"fields": ("first_name", "last_name", "email")},
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
        ("Dates importantes", {"fields": ("last_login", "date_joined",)},),
    )

    def get_readonly_fields(self, request, obj=None):
        # limit editable fields to protect user data, superuser creation must be done using django shell
        if request.user.is_superuser:
            return [
                "email",
                "is_superuser",
            ]
        else:
            return [
                "email",
                "username",
                "user_permissions",
                "is_superuser",
                "is_staff",
                "last_login",
                "date_joined",
            ]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "groups":
            if request.user.is_superuser:
                kwargs["queryset"] = Group.objects.all()
            else:
                kwargs["queryset"] = Group.objects.filter(
                    permitdepartment__integrator=request.user.groups.get(
                        permitdepartment__is_integrator_admin=True
                    ).pk,
                )

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # Only superuser can edit superuser users
    def get_queryset(self, request):
        # Only allow integrator to change users that have no group, are not superuser or are in group administrated by integrator
        if request.user.is_superuser:
            qs = User.objects.all()
        else:
            qs = User.objects.filter(
                Q(is_superuser=False),
                Q(
                    groups__permitdepartment__integrator=request.user.groups.get(
                        permitdepartment__is_integrator_admin=True
                    ).pk
                )
                | Q(groups__isnull=True),
            )
        return qs


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class DepartmentAdminForm(forms.ModelForm):
    class Meta:
        model = models.PermitDepartment
        fields = [
            "description",
            "is_validator",
            "is_default_validator",
            "is_archeologist",
            "administrative_entity",
            "integrator",
            "is_integrator_admin",
        ]
        help_texts = {
            "administrative_entity": _(
                "En tant qu'intégrateur, vous devez tout d'abord créer une entité administrative, pressez simplement sur + "
            ),
        }

    # If the group is updated to be integrator, the users in this group should not be in another integrator group
    def clean(self):
        is_integrator_admin = self.cleaned_data["is_integrator_admin"]
        group = self.cleaned_data["group"]

        # Check only if the group passed from not integrator to integrator
        if self.instance and not self.instance.is_integrator_admin and is_integrator_admin:
            user_with_integrator_group = Group.objects.exclude(pk=group.pk).filter(
                user__in=group.user_set.all(),
                permitdepartment__is_integrator_admin=True,
            ).exists()

            # Raise error if this group is integrator and user(s) is/are already in integrator group and this group
            if user_with_integrator_group:
                raise forms.ValidationError({
                    "is_integrator_admin": MULTIPLE_INTEGRATOR_ERROR_MESSAGE
                })
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
            return ["integrator", "is_integrator_admin"]


class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        help_texts = {
            "permissions": _(
                "Pour un rôle intégrateur, ajoutez toutes les permissions disponibles"
            ),
        }


class GroupAdmin(admin.ModelAdmin):
    inlines = (PermitDepartmentInline,)
    form = GroupAdminForm
 
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

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # permissions that integrator role can grant to group
        if db_field.name == "permissions":
        
            for group in self.model.objects.all():
                existing_permissions = group.permissions.all()
            
            integrator_permissions = Permission.objects.filter(
                codename__in=[
                    "amend_permit_request",
                    "validate_permit_request",
                    "classify_permit_request",
                    "edit_permit_request",
                    "see_private_requests",
                ] 
            )

            if not request.user.is_superuser:
                kwargs["queryset"] = integrator_permissions.union(existing_permissions)

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
        label=_("objets des travaux").capitalize(),
    )


works_object_type_administrative_entities.short_description = _("Communes")


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
            "is_public": forms.RadioSelect(choices=models.PUBLIC_TYPE_CHOICES,),
        }

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

    def save(self, *args, **kwargs):
        for geometry_type in self.GeometryTypes.values:
            setattr(
                self.instance,
                geometry_type,
                geometry_type in self.cleaned_data["geometry_types"],
            )

        return super().save(*args, **kwargs)


class WorksObjectTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    list_display = ["__str__", works_object_type_administrative_entities, "is_public"]
    list_filter = ["administrative_entities"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "works_type",
                    "works_object",
                    "administrative_entities",
                    "is_public",
                    "requires_payment",
                    "integrator",
                )
            },
        ),
        ("Planning et localisation", {"fields": ("geometry_types", "needs_date",)},),
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
    form = WorksObjectTypeAdminForm

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
            "integrator",
            "order",
            "input_type",
            "is_mandatory",
            "works_object_types",
        ]


class WorksObjectPropertyAdmin(
    IntegratorFilterMixin, SortableAdminMixin, admin.ModelAdmin
):
    list_display = ["__str__", "is_mandatory"]
    form = WorksObjectPropertyForm

    # Pass the request from ModelAdmin to ModelForm
    def get_form(
        self, request, obj=None, **kwargs
    ):
        Form = super(WorksObjectPropertyAdmin, self).get_form(request, obj, **kwargs)

        class RequestForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs["user"] = request.user
                return Form(*args, **kwargs)

        return RequestForm


class PermitAdministrativeEntityAdminForm(forms.ModelForm):
    class Meta:
        model = models.PermitAdministrativeEntity
        fields = "__all__"
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
            "is_public": forms.RadioSelect(choices=models.PUBLIC_TYPE_CHOICES,),
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


class WorksObjectAdminForm(forms.ModelForm):
    class Meta:
        model = models.WorksObject
        fields = "__all__"
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


class WorksObjectAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = WorksObjectAdminForm


class PermitAdministrativeEntityAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    form = PermitAdministrativeEntityAdminForm
    inlines = [
        PermitWorkflowStatusInline,
    ]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "integrator":
            kwargs["queryset"] = Group.objects.filter(
                permitdepartment__is_integrator_admin=True,
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PermitRequestAmendPropertyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user")
        super().__init__(*args, **kwargs)
        self.fields["works_object_types"] = get_works_object_types_field(user)

    class Meta:
        model = models.PermitRequestAmendProperty
        fields = ["name", "is_mandatory", "works_object_types", "integrator"]


class PermitRequestAmendPropertyAdmin(IntegratorFilterMixin, admin.ModelAdmin):

    list_display = ["sortable_str", "is_mandatory"]
    form = PermitRequestAmendPropertyForm

    def sortable_str(self, obj):
        return str(obj)

    sortable_str.short_description = (
        "2.2 Configuration des champs de traitement des demandes"
    )
    sortable_str.admin_order_field = "name"

    # Pass the request from ModelAdmin to ModelForm
    def get_form(
        self, request, obj=None, **kwargs
    ):
        Form = super(PermitRequestAmendPropertyAdmin, self).get_form(
            request, obj, **kwargs
        )

        class RequestForm(Form):
            def __new__(cls, *args, **kwargs):
                kwargs["user"] = request.user
                return Form(*args, **kwargs)

        return RequestForm


class PermitActorTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "works_type":
            kwargs["queryset"] = filter_for_user(request.user, models.WorksType.objects.all())
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class WorksTypeAdmin(IntegratorFilterMixin, admin.ModelAdmin):
    pass


admin.site.register(models.PermitActorType, PermitActorTypeAdmin)
admin.site.register(models.WorksType, WorksTypeAdmin)
admin.site.register(models.WorksObjectType, WorksObjectTypeAdmin)
admin.site.register(models.WorksObjectProperty, WorksObjectPropertyAdmin)
admin.site.register(models.PermitAdministrativeEntity, PermitAdministrativeEntityAdmin)
admin.site.register(models.WorksObject, WorksObjectAdmin)
admin.site.register(models.PermitRequestAmendProperty, PermitRequestAmendPropertyAdmin)
