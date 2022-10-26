import logging

from allauth.socialaccount.providers.oauth2.urls import default_urlpatterns
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework import routers

from geocity.apps.accounts.dootix.provider import DootixProvider
from geocity.apps.accounts.geomapfish.provider import GeomapfishProvider
from geocity.apps.django_wfs3.urls import wfs3_router
from geocity.apps.permits import api
from geocity.apps.submissions import views as submissions_views
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
    path("", submissions_views.submission_select_administrative_entity),
    # path("", permits_views.permit_request_select_administrative_entity),
    path("permit-requests/", include("geocity.apps.permits.urls")),
    path("permit-requests-new/", include("geocity.apps.submissions.urls")),
    path("reports/", include("geocity.apps.reports.urls")),
    path("grappelli/", include("grappelli.urls")),  # grappelli URLS
]

urlpatterns += [
    path("", include("geocity.apps.accounts.urls")),
    path(
        "permitauthorcreate/", views.permit_author_create, name="permit_author_create"
    ),
    path("rest/", include(router.urls)),  # Django-rest urls
    path("rest/current_user/", api.CurrentUserAPIView.as_view(), name="current_user"),
    path("wfs3/", include(wfs3_router.urls)),  # Django-rest urls
    path("admin/", admin.site.urls),
]

if settings.PREFIX_URL:
    urlpatterns = [path(settings.PREFIX_URL, include(urlpatterns))]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
