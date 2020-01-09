from django.urls import include, path

from . import views

app_name = 'permits'

permit_request_urlpatterns = [
    path('objects/', views.permit_request_select_objects, name='permit_request_select_objects'),
]

urlpatterns = [
    path('<int:permit_request_id>/', include(permit_request_urlpatterns)),
    path('', include(permit_request_urlpatterns)),
    path('new/', views.create_permit_request, name='permit_request_create'),
]
