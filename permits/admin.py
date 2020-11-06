from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django import forms
from simple_history.admin import SimpleHistoryAdmin
from . import models
from geomapshark import settings
from. import forms as permit_forms
admin.site.register(models.WorksType)
admin.site.register(models.WorksObject)
admin.site.register(models.PermitActorType)
admin.site.register(models.PermitDepartment)
admin.site.register(models.PermitRequestValidation)
admin.site.register(models.GeomLayer)
admin.site.register(models.PermitRequestGeoTime, SimpleHistoryAdmin)
admin.site.register(models.PermitAuthor, SimpleHistoryAdmin)


class PermitRequestHistoryAdmin(SimpleHistoryAdmin):
    list_display = ["id", "administrative_entity", "status"]
    history_list_display = ["status"]
    search_fields = ['administrative_entity', 'user__username']


def works_object_type_administrative_entities(obj):
    return ", ".join(administrative_entity.name for administrative_entity in obj.administrative_entities.all())


works_object_type_administrative_entities.short_description = _("Communes")


class WorksObjectTypeAdmin(admin.ModelAdmin):
    list_display = ['__str__', works_object_type_administrative_entities]
    list_filter = ['administrative_entities']

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('works_object', 'works_type').prefetch_related('administrative_entities')


class WorksObjectTypeWithAdministrativeEntities(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        entities = ", ".join(entity.name for entity in obj.administrative_entities.all())
        return f"{obj.works_object} ({obj.works_type}) - {entities}"


class WorksObjectPropertyForm(forms.ModelForm):
    works_object_types = WorksObjectTypeWithAdministrativeEntities(
        queryset=(
            models.WorksObjectType
                  .objects
                  .select_related('works_object', 'works_type')
                  .order_by('works_object__name', 'works_type__name')
                  .prefetch_related('administrative_entities')
        ),
        widget=forms.CheckboxSelectMultiple,
        label=_('objets des travaux').capitalize(),
    )

    class Meta:
        model = models.WorksObjectProperty
        fields = ['name', 'input_type', 'is_mandatory', 'works_object_types']


class WorksObjectPropertyAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'is_mandatory']
    form = WorksObjectPropertyForm


class PermitAdministrativeEntityAdminForm(forms.ModelForm):

    class Meta:
        model = models.PermitAdministrativeEntity
        fields = '__all__'
        widgets = {
            'general_informations': forms.Textarea(attrs={'rows': 5, }),
            'geom': permit_forms.GeometryWidget(attrs={
                'map_width': '100%',
                'map_height': 400,
                'default_center': [2539057, 1181111],
                'default_zoom': 10,
                'display_raw': False,
                'edit_geom': True,
                'min_zoom': 5,
                'wmts_capabilities_url': settings.WMTS_GETCAP,
                'wmts_layer': settings.WMTS_LAYER,
                'wmts_capabilities_url_alternative': settings.WMTS_GETCAP_ALTERNATIVE,
                'wmts_layer_alternative': settings.WMTS_LAYER_ALTERNATIVE,
                'restriction_area_enabled': False,
                'geometry_db_type': 'MultiPolygon',
            }),
        }



class PermitAdministrativeEntityAdmin(admin.ModelAdmin):
    form = PermitAdministrativeEntityAdminForm


admin.site.register(models.WorksObjectType, WorksObjectTypeAdmin)
admin.site.register(models.WorksObjectProperty, WorksObjectPropertyAdmin)
admin.site.register(models.PermitAdministrativeEntity, PermitAdministrativeEntityAdmin)
admin.site.register(models.PermitRequest, PermitRequestHistoryAdmin)
