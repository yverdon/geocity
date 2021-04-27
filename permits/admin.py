import django.db.models
from adminsortable2.admin import SortableAdminMixin
from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from geomapshark import settings
from simple_history.admin import SimpleHistoryAdmin
from django.contrib.auth.models import Group, User, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import PermissionDenied

from . import forms as permit_forms
from . import models

admin.site.register(models.PermitActorType)
admin.site.register(models.WorksType)

# change the user admin depending on role
class UserAdmin(BaseUserAdmin):
    # exclude = ('lastname',)
    # readonly_fields = ["email", "password", "user_permissions"]

    def get_readonly_fields(self, request, obj=None):
        # FIXME Integrator should be in one and only one group!
        user_groups = Group.objects.filter(user=request.user)
        # limit editable fields to protect user data, superuser creation must be down using django shell
        if request.user.is_superuser:
            return [
                "email",
                "is_superuser",
                "is_staff",
            ]
        if user_groups[0].permitdepartment.is_integrator_admin:
            return [
                "email",
                "username",
                "password",
                "user_permissions",
                "is_superuser",
                "is_staff",
                "last_login",
                "date_joined",
            ]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "groups":
            user_groups = Group.objects.filter(user=request.user)
            kwargs["queryset"] = Group.objects.filter(
                permitdepartment__integrator=user_groups[0].pk
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # FIXME: filte permissions


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Allow a user belonging to integrator group to see only objects created by this group
def get_custom_queryset(self, request, appmodel):
    if request.user.is_superuser:
        qs = appmodel.objects.all()
    else:
        user_groups = Group.objects.filter(user=request.user)
        qs = appmodel.objects.filter(integrator__in=user_groups)
    return qs


# Save the group that created the object
def save_object_whith_creator_group(self, request, obj, form, change):
    # FIXME: warn the super user that he can't create this setting as only integrators can
    user_group = Group.objects.get(user=request.user)
    obj.integrator = user_group
    obj.save()


# Inline for group & department (1to1)
class PermitDepartmentInline(admin.StackedInline):
    model = models.PermitDepartment
    can_delete = False
    verbose_name_plural = "Service"
    inline_classes = ("collapse open",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "administrative_entity":
            user_groups = Group.objects.filter(user=request.user)
            kwargs["queryset"] = models.PermitAdministrativeEntity.objects.filter(
                integrator=user_groups[0].pk
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["is_integrator_admin", "integrator"]


# Define a new Group admin
class GroupAdmin(admin.ModelAdmin):
    inlines = (PermitDepartmentInline,)

    class Meta:
        model = Group

    # FIXME: filter admintrative entity
    # FIXME:
    def get_queryset(self, request):

        if request.user.is_superuser:
            qs = Group.objects.all()
        else:
            user_groups = Group.objects.filter(user=request.user)
            user_departments = models.PermitDepartment.objects.filter(
                integrator__in=user_groups
            ).values_list("id", flat=True)
            qs = Group.objects.filter(pk__in=user_departments)
        return qs

    def save_model(self, request, obj, form, change):
        # FIXME: handle the multi group integrator user ?
        # FIXME: warn the super user that he can't create this setting as only integrators can
        user_groups = Group.objects.filter(user=request.user)

        if (
            user_groups[0].permitdepartment.is_integrator_admin
            and len(user_groups) == 1
        ):
            obj.permitdepartment.integrator = user_groups[0].pk
            obj.save()
        else:
            raise PermissionDenied

        # Integrator role can only be created by superadmin.
        if request.user.is_superuser and obj.permitdepartment.is_integrator_admin:
            # FIXME: check that user is in oe and only one group
            obj.permissions.set(
                # FIXME be more specific
                Permission.objects.all()
            )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # permissions that integrator role can assign to group
        if db_field.name == "permissions":
            kwargs["queryset"] = Permission.objects.filter(
                codename__in=[
                    "amend_permit_request",
                    "validate_permit_request",
                    "classify_permit_request",
                    "edit_permit_request",
                ]
            )
        return super().formfield_for_manytomany(db_field, request, **kwargs)


# Re-register GroupAdmin
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)


def works_object_type_administrative_entities(obj):
    return ", ".join(
        administrative_entity.name
        for administrative_entity in obj.administrative_entities.all()
    )


def get_works_object_types_field():
    return WorksObjectTypeWithAdministrativeEntitiesField(
        queryset=(
            models.WorksObjectType.objects.select_related("works_object", "works_type")
            .order_by("works_object__name", "works_type__name")
            .prefetch_related("administrative_entities")
        ),
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


class WorksObjectTypeAdmin(admin.ModelAdmin):
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
    # FIXME: special case fr yc-250
    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("works_object", "works_type")
            .prefetch_related("administrative_entities")
        )

    def save_model(self, request, obj, form, change):
        save_object_whith_creator_group(self, request)


class WorksObjectTypeWithAdministrativeEntitiesField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        entities = ", ".join(
            entity.name for entity in obj.administrative_entities.all()
        )
        return f"{obj.works_object} ({obj.works_type}) - {entities}"


class WorksObjectPropertyForm(forms.ModelForm):
    works_object_types = get_works_object_types_field()

    class Meta:
        model = models.WorksObjectProperty
        fields = [
            "name",
            "placeholder",
            "help_text",
            "order",
            "input_type",
            "is_mandatory",
            "works_object_types",
        ]


class WorksObjectPropertyAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ["__str__", "is_mandatory"]
    form = WorksObjectPropertyForm

    def get_queryset(self, request):
        return get_custom_queryset(self, request, models.WorksObjectProperty)

    def save_model(self, request, obj, form, change):
        save_object_whith_creator_group(self, request, obj, form, change)


class PermitAdministrativeEntityAdminForm(forms.ModelForm):
    class Meta:
        model = models.PermitAdministrativeEntity
        fields = "__all__"
        exclude = ["enabled_status", "integrator"]
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


class WorksObjectAdmin(admin.ModelAdmin):
    form = WorksObjectAdminForm

    def get_queryset(self, request):
        return get_custom_queryset(self, request, models.WorksObject)

    def save_model(self, request, obj, form, change):
        save_object_whith_creator_group(self, request, obj, form, change)


class PermitAdministrativeEntityAdmin(admin.ModelAdmin):
    form = PermitAdministrativeEntityAdminForm
    inlines = [
        PermitWorkflowStatusInline,
    ]

    def get_queryset(self, request):

        if request.user.is_superuser:
            qs = models.PermitAdministrativeEntity.objects.all()
        else:
            user_groups = Group.objects.filter(user=request.user)
            qs = models.PermitAdministrativeEntity.objects.filter(
                integrator__in=user_groups
            )
        return qs

    def get_queryset(self, request):
        return get_custom_queryset(self, request, models.PermitAdministrativeEntity)

    def save_model(self, request, obj, form, change):
        save_object_whith_creator_group(self, request, obj, form, change)


class PermitRequestAmendPropertyForm(forms.ModelForm):
    works_object_types = get_works_object_types_field()

    class Meta:
        model = models.PermitRequestAmendProperty
        # FIXME: show the integrator field for superuser ?
        fields = ["name", "is_mandatory", "works_object_types", "integrator"]


class PermitRequestAmendPropertyAdmin(admin.ModelAdmin):

    list_display = ["sortable_str", "is_mandatory"]
    form = PermitRequestAmendPropertyForm

    def sortable_str(self, obj):
        return str(obj)

    sortable_str.short_description = (
        "2.2 Configuration des champs de traitement des demandes"
    )
    sortable_str.admin_order_field = "name"
    readonly_fields = ["integrator"]

    def get_queryset(self, request):
        return get_custom_queryset(self, request, models.PermitRequestAmendProperty)

    def save_model(self, request, obj, form, change):
        save_object_whith_creator_group(self, request, obj, form, change)


admin.site.register(models.WorksObjectType, WorksObjectTypeAdmin)
admin.site.register(models.WorksObjectProperty, WorksObjectPropertyAdmin)
admin.site.register(models.PermitAdministrativeEntity, PermitAdministrativeEntityAdmin)
admin.site.register(models.WorksObject, WorksObjectAdmin)
admin.site.register(models.PermitRequestAmendProperty, PermitRequestAmendPropertyAdmin)
