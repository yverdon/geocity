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
from django.forms import ValidationError

from . import forms as permit_forms
from . import models


class UserAdmin(BaseUserAdmin):
    def get_readonly_fields(self, request, obj=None):
        # limit editable fields to protect user data, superuser creation must be down using django shell
        if request.user.is_superuser:
            return [
                "email",
                "is_superuser",
                "is_staff",
            ]
        else:
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
            if not request.user.is_superuser:
                kwargs["queryset"] = Group.objects.filter(
                    permitdepartment__integrator=request.user.groups.all()[0].pk,
                    permitdepartment__is_integrator_admin=False,
                )
            else:
                kwargs["queryset"] = Group.objects.all()

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    # Only superuser can edit superuser users
    def get_queryset(self, request):

        if not request.user.is_superuser:
            qs = User.objects.filter(is_superuser=False)
        else:
            qs = User.objects.all()
        return qs

    def save_model(self, request, obj, form, change):

        edited_user_groups = Group.objects.filter(
            pk__in=obj.groups.values_list("id", flat=True)
        )
        is_integrator_admin = False

        for group in edited_user_groups:
            if group.permitdepartment.is_integrator_admin:
                is_integrator_admin = True

        # FIXME be less violent with the user...
        if obj.groups.count() > 1 and is_integrator_admin:
            raise ValidationError(
                _(
                    "Un utilisateur membre d'un groupe de type 'Intégrateur' ne peut être que dans un et uniquement un groupe"
                ),
                code="invalid",
            )
        else:
            obj.save()


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Allow a user belonging to integrator group to see only objects created by this group
# FIXME: what sould the superuser see / edit ?
def get_custom_queryset(self, request, appmodel):
    if request.user.is_superuser:
        qs = appmodel.objects.all()
    else:
        qs = appmodel.objects.filter(integrator__in=request.user.groups.all())
    return qs


# Save the group that created the object
def save_object_whith_creator_group(self, request, obj, form, change):
    obj.integrator = request.user.groups.all()[0]
    obj.save()


# Inline for group & department (1to1)
class PermitDepartmentInline(admin.StackedInline):
    model = models.PermitDepartment
    can_delete = False
    verbose_name_plural = "Service"
    inline_classes = ("collapse open",)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "administrative_entity":
            if not request.user.is_superuser:
                kwargs["queryset"] = models.PermitAdministrativeEntity.objects.filter(
                    integrator=request.user.groups.all()[0].pk
                )
            else:
                kwargs["queryset"] = models.PermitAdministrativeEntity.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["is_integrator_admin", "integrator"]
        else:
            return []


# Define a new Group admin
class GroupAdmin(admin.ModelAdmin):
    inlines = (PermitDepartmentInline,)

    class Meta:
        model = Group

    def get_queryset(self, request):

        if request.user.is_superuser:
            qs = Group.objects.all()
        else:
            user_departments = models.PermitDepartment.objects.filter(
                integrator__in=request.user.groups.all()
            ).values_list("id", flat=True)
            qs = Group.objects.filter(pk__in=user_departments)
        return qs

    def save_model(self, request, obj, form, change):

        if not request.user.is_superuser:
            user_groups = request.user.groups.all()

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
                    "requires_payment",
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
        if not request.user.is_superuser:
            qs = qs.filter(integrator__in=request.user.groups.all())
        return qs

    def save_model(self, request, obj, form, change):
        save_object_whith_creator_group(self, request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["integrator"]
        else:
            return []

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "administrative_entities":
            if not request.user.is_superuser:
                kwargs["queryset"] = models.PermitAdministrativeEntity.objects.filter(
                    integrator=request.user.groups.all()[0].pk
                )
            else:
                kwargs["queryset"] = models.PermitAdministrativeEntity.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "works_type":
            if not request.user.is_superuser:
                kwargs["queryset"] = models.WorksType.objects.filter(
                    integrator=request.user.groups.all()[0].pk
                )
            else:
                kwargs["queryset"] = models.WorksType.objects.all()

        if db_field.name == "works_object":
            if not request.user.is_superuser:
                kwargs["queryset"] = models.WorksObject.objects.filter(
                    integrator=request.user.groups.all()[0].pk
                )
            else:
                kwargs["queryset"] = models.WorksObject.objects.all()

        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["integrator"]
        else:
            return []

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "works_object_types":
            # FIXME: filtering is not ok!
            if not request.user.is_superuser:
                kwargs["queryset"] = models.WorksObjectType.objects.filter(
                    integrator=request.user.groups.all()[0].pk
                )
            else:
                kwargs["queryset"] = models.WorksObjectType.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["integrator"]
        else:
            return []


class PermitAdministrativeEntityAdmin(admin.ModelAdmin):
    form = PermitAdministrativeEntityAdminForm
    inlines = [
        PermitWorkflowStatusInline,
    ]

    def get_queryset(self, request):

        if request.user.is_superuser:
            qs = models.PermitAdministrativeEntity.objects.all()
        else:
            qs = models.PermitAdministrativeEntity.objects.filter(
                integrator__in=request.user.groups.all()
            )
        return qs

    def get_queryset(self, request):
        return get_custom_queryset(self, request, models.PermitAdministrativeEntity)

    def save_model(self, request, obj, form, change):
        save_object_whith_creator_group(self, request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["integrator"]
        else:
            return []


class PermitRequestAmendPropertyForm(forms.ModelForm):
    works_object_types = get_works_object_types_field()

    class Meta:
        model = models.PermitRequestAmendProperty
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

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "works_object_types":
            # FIXME: filtering is not ok!
            if not request.user.is_superuser:
                print("icicci")
                kwargs["queryset"] = models.WorksObjectType.objects.filter(
                    integrator=request.user.groups.all()[0].pk
                )
            else:
                kwargs["queryset"] = models.WorksObjectType.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class PermitActorTypeAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        # FIXME: filter not ok on list
        return get_custom_queryset(self, request, models.PermitActorType)

    def save_model(self, request, obj, form, change):
        save_object_whith_creator_group(self, request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["integrator"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "works_type":
            if not request.user.is_superuser:
                kwargs["queryset"] = models.WorksType.objects.filter(
                    integrator=request.user.groups.all()[0].pk
                )
            else:
                kwargs["queryset"] = models.WorksType.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class WorksTypeAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return get_custom_queryset(self, request, models.WorksType)

    def save_model(self, request, obj, form, change):
        save_object_whith_creator_group(self, request, obj, form, change)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ["integrator"]
        else:
            return []


# FIXME only super user should be allowed to change constance fields

admin.site.register(models.PermitActorType, PermitActorTypeAdmin)
admin.site.register(models.WorksType, WorksTypeAdmin)
admin.site.register(models.WorksObjectType, WorksObjectTypeAdmin)
admin.site.register(models.WorksObjectProperty, WorksObjectPropertyAdmin)
admin.site.register(models.PermitAdministrativeEntity, PermitAdministrativeEntityAdmin)
admin.site.register(models.WorksObject, WorksObjectAdmin)
admin.site.register(models.PermitRequestAmendProperty, PermitRequestAmendPropertyAdmin)
