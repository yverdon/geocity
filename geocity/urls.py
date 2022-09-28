import logging

from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework import routers

from geocity.apps.accounts.dootix.provider import DootixProvider
from geocity.apps.accounts.geomapfish.provider import GeomapfishProvider
from geocity.apps.django_wfs3.urls import wfs3_router
from geocity.apps.permits import api
from geocity.apps.permits import views as permits_views
from geocity.apps.permits.admin import PermitsAdminSite

from . import views

logger = logging.getLogger(__name__)

admin.site = PermitsAdminSite()


# See TWO_FACTOR_PATCH_ADMIN
if settings.ENABLE_2FA:
    from .admin_site import AdminSiteOTPRequiredMixinRedirSetup

    admin.site.__class__ = AdminSiteOTPRequiredMixinRedirSetup


# Django-rest Configuration

router = routers.DefaultRouter()
router.register(r"events", api.PermitRequestGeoTimeViewSet, "events")
router.register(r"permits", api.PermitRequestViewSet, "permits")
router.register(r"permits_point", api.PermitRequestPointViewSet, "permit_point")
router.register(r"permits_line", api.PermitRequestLineViewSet, "permit_line")
router.register(r"permits_poly", api.PermitRequestPolyViewSet, "permit_poly")
router.register(r"search", api.SearchViewSet, "search")
router.register(r"permits_details", api.PermitRequestDetailsViewSet, "permits_details")

# Django-configuration
urlpatterns = [
    path("", permits_views.permit_request_select_administrative_entity),
    path("permit-requests/", include("geocity.apps.permits.urls")),
    path("reports/", include("geocity.apps.reports.urls")),
    path("grappelli/", include("grappelli.urls")),  # grappelli URLS
]

if settings.ENABLE_2FA:
    from two_factor.urls import urlpatterns as tf_urls
    from two_factor.views import ProfileView, SetupCompleteView

    logger.info("2 factors authentication is enabled")
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
        path(
            "account/duo_callback/",
            views.DuoCallbackView.as_view(),
            name="duo_callback",
        ),
        path("", include(tf_urls)),
    ]
else:
    logger.info("2 factors authentication is disabled")
    urlpatterns += [
        path(
            "account/login/",
            views.CustomLoginView.as_view(template_name="registration/login.html"),
            name="account_login",
        ),
    ]

urlpatterns += (
    [
        path("accounts/social/", include("allauth.socialaccount.urls")),
    ]
    + default_urlpatterns(GeomapfishProvider)
    + default_urlpatterns(DootixProvider)
)

urlpatterns += [
    path(
        "account/logout/",
        views.logout_view,
        name="logout",
    ),
    path(
        "account/lockout/",
        views.lockout_view,
        name="lockout",
    ),
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
        "account/activate/<uid>/<token>/",
        views.ActivateAccountView.as_view(),
        name="activate_account",
    ),
    path(
        "permitauthorcreate/", views.permit_author_create, name="permit_author_create"
    ),
    path("permitauthoredit/", views.permit_author_edit, name="permit_author_edit"),
    path("account/", include("django.contrib.auth.urls")),
    path("rest/", include(router.urls)),  # Django-rest urls
    path("rest/current_user/", api.CurrentUserAPIView.as_view(), name="current_user"),
    path("wfs3/", include(wfs3_router.urls)),  # Django-rest urls
    path("admin/", admin.site.urls),
    path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("captcha/", include("captcha.urls")),
    path("api-tokens/", include("knox.urls")),
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
