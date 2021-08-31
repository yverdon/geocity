import logging

from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework import routers

from accounts.geomapfish.provider import GeomapfishProvider
from accounts.dootix.provider import DootixProvider
from permits import api
from permits import views as permits_views

from . import views

logger = logging.getLogger(__name__)


# See TWO_FACTOR_PATCH_ADMIN
if settings.ENABLE_2FA:
    from .admin_site import AdminSiteOTPRequiredMixinRedirSetup

    admin.site.__class__ = AdminSiteOTPRequiredMixinRedirSetup


# Django-rest Configuration

router = routers.DefaultRouter()
router.register(r"events", api.PermitRequestGeoTimeViewSet, "events")
router.register(r"front-config", api.GeocityViewConfigViewSet, "front-config")
router.register(r"permits", api.PermitRequestViewSet, "permits")


# Django-configuration
urlpatterns = [
    path("", permits_views.permit_request_select_administrative_entity),
    path("permit-requests/", include("permits.urls")),
    path("grappelli/", include("grappelli.urls")),  # grappelli URLS
]

if settings.ENABLE_2FA:
    from two_factor.urls import urlpatterns as tf_urls
    from two_factor.views import LoginView, ProfileView, SetupCompleteView

    logger.info("2 factors authentification is enabled")
    urlpatterns += [
        path(
            "account/login/",
            views.CustomLoginView.as_view(template_name="two_factor/login.html"),
            name="account_login",
        ),
        path(
            "account/two_factor/",
            ProfileView.as_view(template_name="two_factor/profile.html"),
            name="profile",
        ),
        path(
            "account/two_factor/setup/complete/",
            SetupCompleteView.as_view(template_name="two_factor/setup_complete.html"),
            name="setup_complete",
        ),
        path("", include(tf_urls)),
    ]
else:
    logger.info("2 factors authentification is disabled")
    urlpatterns += [
        path(
            "account/login/",
            views.CustomLoginView.as_view(template_name="registration/login.html"),
            name="account_login",
        ),
    ]

urlpatterns += (
    [path("accounts/social/", include("allauth.socialaccount.urls")),]
    + default_urlpatterns(GeomapfishProvider)
    + default_urlpatterns(DootixProvider)
)

urlpatterns += [
    path("account/logout/", views.logout_view, name="logout",),
    path(
        "account/password_reset/",
        views.CustomPasswordResetView.as_view(
            template_name="registration/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "account/password_reset_confirm/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "account/password_reset/done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "account/password_reset/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "account/password_change/",
        auth_views.PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "permitauthorcreate/", views.permit_author_create, name="permit_author_create"
    ),
    path("permitauthoredit/", views.permit_author_edit, name="permit_author_edit"),
    path("account/", include("django.contrib.auth.urls")),
    path("rest/", include(router.urls)),  # Django-rest urls
    path("admin/", admin.site.urls),
    path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]

if settings.PREFIX_URL:
    urlpatterns = [path(settings.PREFIX_URL, include(urlpatterns))]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = (
        [path("__debug__/", include(debug_toolbar.urls))]
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + urlpatterns
    )
