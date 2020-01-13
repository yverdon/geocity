from django.urls import include, path

from . import views

app_name = 'permits'

permit_request_urlpatterns = [
    path('types/', views.permit_request_select_types, name='permit_request_select_types'),
    path('objects/', views.permit_request_select_objects, name='permit_request_select_objects'),
]

existing_permit_request_urlpatterns = [
    path('properties/', views.permit_request_properties, name='permit_request_properties'),
    path('appendices/', views.permit_request_appendices, name='permit_request_appendices'),
]

urlpatterns = [
    path('<int:permit_request_id>/', include(permit_request_urlpatterns + existing_permit_request_urlpatterns)),
    path('', include(permit_request_urlpatterns)),
]
