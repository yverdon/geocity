import logging

from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from geocity.apps.accounts.dootix.provider import DootixProvider
from geocity.apps.accounts.geomapfish.provider import GeomapfishProvider
from geocity.apps.permits import routers
from geocity.apps.permits import views as permits_views
from geocity.apps.permits.admin import PermitsAdminSite

from . import views

logger = logging.getLogger(__name__)


# See TWO_FACTOR_PATCH_ADMIN
if settings.ENABLE_2FA:
    from .admin_site import OTPRequiredPermitsAdminSite

    logger.info("2 factors authentification is enabled")
    admin.site = OTPRequiredPermitsAdminSite()
else:
    logger.info("2 factors authentification is disabled")
    admin.site = PermitsAdminSite()


# Django-configuration
urlpatterns = [
    path(
        "",
        permits_views.permit_request_select_administrative_entity,
    ),
    path(
        "permit-requests/",
        include("geocity.apps.permits.urls"),
    ),
    path(
        "reports/",
        include("geocity.apps.reports.urls"),
    ),
    path(
        "grappelli/",
        include("grappelli.urls"),
    ),
    path(
        "accounts/social/",
        include("allauth.socialaccount.urls"),
    ),
    # Not too why these need to be added manually here ? isn't allauth supposed to include them
    # for all configured providers ? Otherwise how would new providers be available ?
    *default_urlpatterns(GeomapfishProvider),
    *default_urlpatterns(DootixProvider),
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
        "permitauthorcreate/",
        views.permit_author_create,
        name="permit_author_create",
    ),
    path(
        "permitauthoredit/",
        views.permit_author_edit,
        name="permit_author_edit",
    ),
    path(
        "account/",
        include("django.contrib.auth.urls"),
    ),
    path(
        "rest/",
        include(routers.default.urls),
    ),
    path(
        "wfs3/",
        include(routers.wfs3.urls),
    ),
    path(
        "admin/",
        admin.site.urls,
    ),
    path(
        "oauth/",
        include("oauth2_provider.urls", namespace="oauth2_provider"),
    ),
    path(
        "captcha/",
        include("captcha.urls"),
    ),
    path(
        "api-tokens/",
        include("knox.urls"),
    ),
]

if settings.ENABLE_2FA:
    from two_factor.urls import urlpatterns as tf_urls
    from two_factor.views import ProfileView, SetupCompleteView

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
            "",
            include(tf_urls),
        ),
    ]
else:
    urlpatterns += [
        path(
            "account/login/",
            views.CustomLoginView.as_view(template_name="registration/login.html"),
            name="account_login",
        ),
    ]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(
            "__debug__/",
            include(debug_toolbar.urls),
        ),
    ]

if settings.PREFIX_URL:
    urlpatterns = [path(settings.PREFIX_URL, include(urlpatterns))]
