import logging

from django.conf import settings
from django.contrib import admin
from django.urls import include, path

import geocity.apps.api.urls
from geocity.apps.django_wfs3.urls import wfs3_router
from geocity.apps.submissions import views as submissions_views

from .admin_site import PermitsAdminSite

logger = logging.getLogger(__name__)

admin.site = PermitsAdminSite()

# See TWO_FACTOR_PATCH_ADMIN
if settings.ENABLE_2FA:
    from .admin_site_2fa import AdminSiteOTPRequiredMixinRedirSetup
    admin.site = AdminSiteOTPRequiredMixinRedirSetup()


# Django-rest Configuration


# Django-configuration
urlpatterns = [
    path("", submissions_views.submission_select_administrative_entity),
    path("permit-requests/", include("geocity.apps.submissions.urls")),
    path("reports/", include("geocity.apps.reports.urls")),
    path("grappelli/", include("grappelli.urls")),  # grappelli URLS
]

urlpatterns += [
    path("", include("geocity.apps.accounts.urls")),
    path("rest/", include(geocity.apps.api.urls)),  # Django-rest urls
    path("wfs3/", include(wfs3_router.urls)),  # Django-rest urls
    path("captcha/", include("captcha.urls")),
    path("api-tokens/", include("knox.urls")),
    path("account/", include("django.contrib.auth.urls")),
    path("oauth/", include("oauth2_provider.urls", namespace="oauth2_provider")),
    path("admin/", admin.site.urls),
]

if settings.PREFIX_URL:
    urlpatterns = [path(settings.PREFIX_URL, include(urlpatterns))]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
