from django.contrib import admin
from django.urls import include, path
from two_factor.urls import urlpatterns as tf_urls
from two_factor.views import LoginView, ProfileView
from . import settings, views
from permits import views as permits_views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from permits import geoviews

# Django-rest Configuration

router = routers.DefaultRouter()
router.register(r'events', geoviews.PermitRequestGeoTimeViewSet, 'events')
router.register(r'front-config', geoviews.GeocityViewConfigViewSet, 'front-config')

# Django-configuration

urlpatterns = [
    path('', permits_views.permit_request_select_administrative_entity),
    path('permit-requests/', include('permits.urls')),
    path('grappelli/', include('grappelli.urls')),  # grappelli URLS
    path('admin/', admin.site.urls),
    path('account/login/', LoginView.as_view(template_name='registration/login.html'), name='login'), # two factor
    path('account/two_factor/', ProfileView.as_view(template_name='two_factor/profile.html'), name='profile'),
    path('account/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('account/password_reset/', views.CustomPasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('account/password_reset_confirm/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account/password_reset/done', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('account/password_reset/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('account/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('permitauthorcreate/', views.permit_author_create, name='permit_author_create'),
    path('permitauthoredit/', views.permit_author_edit, name='permit_author_edit'),
    path('account/', include('django.contrib.auth.urls')),
    path('rest/', include(router.urls)), # Django-rest urls
    path('', include(tf_urls)), # account/login/ and account/two_factor/ overriden hereabove
]

if settings.PREFIX_URL:
    urlpatterns = [path(settings.PREFIX_URL, include(urlpatterns))]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
