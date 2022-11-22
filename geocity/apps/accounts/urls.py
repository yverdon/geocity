import logging

from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

logger = logging.getLogger(__name__)

app_name = "accounts"

urlpatterns = []

if settings.ENABLE_2FA:
    from two_factor.views import ProfileView, SetupCompleteView

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
        "account/password_reset/done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
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
    path("profile/create/", views.user_profile_create, name="user_profile_create"),
    path("profile/edit/", views.user_profile_edit, name="user_profile_edit"),
    path(
        "admin-data/<path:path>",
        views.administrative_entity_file_download,
        name="administrative_entity_file_download",
    ),
]
