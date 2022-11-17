from geocity.apps.api import views as api_views

from .routers import WFS3Router

wfs3_router = WFS3Router()
wfs3_router.register(r"submissions", api_views.SubmissionViewSet, "submissions")
wfs3_router.register(
    r"submissions_point", api_views.SubmissionPointViewSet, "submissions_point"
)
wfs3_router.register(
    r"submissions_line", api_views.SubmissionLineViewSet, "submissions_line"
)
wfs3_router.register(
    r"submissions_poly", api_views.SubmissionPolyViewSet, "submissions_poly"
)
