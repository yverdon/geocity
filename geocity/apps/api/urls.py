from django.urls import path
from rest_framework import routers

from . import views

router = routers.DefaultRouter()

router.register(r"events", views.SubmissionGeoTimeViewSet, "events")
router.register(r"submissions", views.SubmissionViewSet, "submissions")
router.register(r"submissions_point", views.SubmissionPointViewSet, "submission_point")
router.register(r"submissions_line", views.SubmissionLineViewSet, "submission_line")
router.register(r"submissions_poly", views.SubmissionPolyViewSet, "submission_poly")
router.register(r"search", views.SearchViewSet, "search")
router.register(
    r"submissions_details", views.SubmissionDetailsViewSet, "submissions_details"
)
router.register(r"agenda", views.AgendaViewSet, "agenda")

urlpatterns = router.urls + [
    path("current_user/", views.CurrentUserAPIView.as_view(), name="current_user"),
    path(
        "image/<int:form_id>/<str:image_name>",
        views.image_display,
        name="image_display",
    ),
]
