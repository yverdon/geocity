from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import MapWidgetConfiguration


@login_required
def map_widget_configuration(request, form_id):

    form_map_widget_configuration = MapWidgetConfiguration.objects.get(
        map_widget_configuration_form__pk=form_id
    )

    # TODO: get existing configuration for administrative entity and override JSON with specific keys

    return JsonResponse(form_map_widget_configuration.configuration, safe=False)
