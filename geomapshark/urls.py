from django.contrib import admin
from django.urls import include, path, reverse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.utils.http import is_safe_url
from two_factor.urls import urlpatterns as tf_urls
from two_factor.views import LoginView, ProfileView
from two_factor.admin import AdminSiteOTPRequired, AdminSiteOTPRequiredMixin
from . import settings, views
from permits import views as permits_views
from django.contrib.auth import views as auth_views
from rest_framework import routers
from permits import geoviews


# https://github.com/Bouke/django-two-factor-auth/issues/219#issuecomment-494382380
# Remove when https://github.com/Bouke/django-two-factor-auth/pull/370 is merged
class AdminSiteOTPRequiredMixinRedirSetup(AdminSiteOTPRequired):
    def login(self, request, extra_context=None):
        redirect_to = request.POST.get(
            REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME)
        )
        # For users not yet verified the AdminSiteOTPRequired.has_permission
        # will fail. So use the standard admin has_permission check:
        # (is_active and is_staff) and then check for verification.
        # Go to index if they pass, otherwise make them setup OTP device.
        if request.method == "GET" and super(
            AdminSiteOTPRequiredMixin, self
        ).has_permission(request):
            # Already logged-in and verified by OTP
            if request.user.is_verified():
                # User has permission
                index_path = reverse("admin:index", current_app=self.name)
            else:
                # User has permission but no OTP set:
                index_path = reverse("two_factor:setup", current_app=self.name)
            return HttpResponseRedirect(index_path)

        if not redirect_to or not is_safe_url(
            url=redirect_to, allowed_hosts=[request.get_host()]
        ):
            redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

        return redirect_to_login(redirect_to)


# See TWO_FACTOR_PATCH_ADMIN
admin.site.__class__ = AdminSiteOTPRequiredMixinRedirSetup


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
    path('admin/', admin.site.urls),
]

if settings.PREFIX_URL:
    urlpatterns = [path(settings.PREFIX_URL, include(urlpatterns))]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
