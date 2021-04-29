import django.db.models
from adminsortable2.admin import SortableAdminMixin
from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from geomapshark import settings
from simple_history.admin import SimpleHistoryAdmin

from . import forms as permit_forms
from . import models

admin.site.register(models.PermitActorType)
admin.site.register(models.WorksType)
admin.site.register(models.PermitDepartment)
admin.site.register(models.PermitRequestValidation)
admin.site.register(models.GeomLayer)
admin.site.register(models.PermitRequestGeoTime, SimpleHistoryAdmin)
admin.site.register(models.PermitAuthor, SimpleHistoryAdmin)


class PermitRequestHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "administrative_entity", "status"]
    history_list_display = ["status"]
    search_fields = ["administrative_entity", "user__username"]


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
        return (
            super()
            .get_queryset(request)
            .select_related("works_object", "works_type")
            .prefetch_related("administrative_entities")
        )


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


class WorksObjectAdmin(admin.ModelAdmin):
    form = WorksObjectAdminForm


class PermitAdministrativeEntityAdmin(admin.ModelAdmin):
    form = PermitAdministrativeEntityAdminForm
    inlines = [
        PermitWorkflowStatusInline,
    ]


class PermitRequestAmendPropertyForm(forms.ModelForm):
    works_object_types = get_works_object_types_field()

    class Meta:
        model = models.PermitRequestAmendProperty
        fields = ["name", "is_mandatory", "works_object_types"]


class PermitRequestAmendPropertyAdmin(admin.ModelAdmin):

    list_display = ["sortable_str", "is_mandatory"]
    form = PermitRequestAmendPropertyForm

    def sortable_str(self, obj):
        return str(obj)

    sortable_str.short_description = (
        "2.2 Configuration des champs de traitement des demandes"
    )
    sortable_str.admin_order_field = "name"


admin.site.register(models.PermitRequest, PermitRequestHistoryAdmin)
admin.site.register(models.WorksObjectType, WorksObjectTypeAdmin)
admin.site.register(models.WorksObjectProperty, WorksObjectPropertyAdmin)
admin.site.register(models.PermitAdministrativeEntity, PermitAdministrativeEntityAdmin)
admin.site.register(models.WorksObject, WorksObjectAdmin)
admin.site.register(models.PermitRequestAmendProperty, PermitRequestAmendPropertyAdmin)
