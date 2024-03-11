import logging

from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

import geocity.apps.api.urls
from geocity.apps.accounts.dootix.provider import DootixProvider
from geocity.apps.accounts.geomapfish.provider import GeomapfishProvider
from geocity.apps.django_wfs3.urls import wfs3_router
from geocity.apps.submissions import views as submissions_views

from .views import legacy_urls_redirect

logger = logging.getLogger(__name__)

# See TWO_FACTOR_PATCH_ADMIN
if settings.ENABLE_2FA:
    from .admin_site_2fa import AdminSiteOTPRequiredMixinRedirSetup

    admin.site = AdminSiteOTPRequiredMixinRedirSetup()


# Django-configuration
urlpatterns = [
    path("", submissions_views.submission_select_administrative_entity),
    path("submissions/", include("geocity.apps.submissions.urls")),
    path("forms/", include("geocity.apps.forms.urls")),
    path("reports/", include("geocity.apps.reports.urls")),
    # Backward compatibility for Geocity < 2.1, will be deprecated in 3.0
    re_path(r"permit-requests/.*", legacy_urls_redirect),
]

# Append default urlpatterns for external providers
urlpatterns = (
    urlpatterns
    + default_urlpatterns(GeomapfishProvider)
    + default_urlpatterns(DootixProvider)
)


urlpatterns += [
    path("", include("geocity.apps.accounts.urls", namespace="accounts")),
    path("rest/", include(geocity.apps.api.urls)),  # Django-rest urls
    path("wfs3/", include(wfs3_router.urls)),  # Django-rest urls
    path("captcha/", include("captcha.urls")),
    path("api-tokens/", include("knox.urls")),
    path("account/", include("django.contrib.auth.urls")),
    path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("admin/", admin.site.urls),
    path("accounts/social/", include("allauth.socialaccount.urls")),
    path(
        "ckeditor5/", include("django_ckeditor_5.urls"), name="ck_editor_5_upload_file"
    ),
]

if settings.ENABLE_2FA:
    from two_factor.urls import urlpatterns as tf_urls

    urlpatterns += [
        path("", include(tf_urls)),
    ]

if settings.PREFIX_URL:
    urlpatterns = [path(settings.PREFIX_URL, include(urlpatterns))]

if settings.DEBUG:
    urlpatterns = [path("__debug__/", include("debug_toolbar.urls"))] + urlpatterns
