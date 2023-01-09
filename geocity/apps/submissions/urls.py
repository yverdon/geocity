from django.urls import include, path

from . import views

app_name = "submissions"

submission_urlpatterns = [
    path(
        "administrative-entity/",
        views.submission_select_administrative_entity,
        name="submission_select_administrative_entity",
    ),
]

anonymous_submission_urlpatterns = [
    path(
        "anonymous/",
        views.anonymous_submission,
        name="anonymous_submission",
    ),
    path(
        "anonymous/sent",
        views.anonymous_submission_sent,
        name="anonymous_submission_sent",
    ),
]

existing_submission_urlpatterns = [
    path("", views.SubmissionDetailView.as_view(), name="submission_detail"),
    path(
        "objects/",
        views.submission_select_forms,
        name="submission_select_forms",
    ),
    path("properties/", views.submission_fields, name="submission_fields"),
    path("appendices/", views.submission_appendices, name="submission_appendices"),
    path("actors/", views.submission_contacts, name="submission_contacts"),
    path("submit/", views.submission_submit, name="submission_submit"),
    path(
        "submitconfirmed/",
        views.submission_submit_confirmed,
        name="submission_submit_confirmed",
    ),
    path("geotime/", views.submission_geo_time, name="submission_geo_time"),
    path("delete/", views.submission_delete, name="submission_delete"),
    path("approve/", views.submission_approve, name="submission_approve"),
    path("reject/", views.submission_reject, name="submission_reject"),
    path(
        "prolongation/",
        views.submission_prolongation,
        name="submission_prolongation",
    ),
]

urlpatterns = [
    path(
        "<int:submission_id>/",
        include(submission_urlpatterns + existing_submission_urlpatterns),
    ),
    path(
        "permits-files/<path:path>",
        views.submission_file_download,
        name="submission_file_download",
    ),
    path(
        "form-files/<path:path>",
        views.field_file_download,
        name="field_file_download",
    ),
    path(
        "documents/<path:path>/download",
        views.ComplementaryDocumentDownloadView.as_view(),
        name="complementary_documents_download",
    ),
    path(
        "documents/<int:pk>/delete",
        views.submission_complementary_document_delete,
        name="complementary_documents_delete",
    ),
    path("", views.SubmissionList.as_view(), name="submissions_list"),
    path("", include(submission_urlpatterns + anonymous_submission_urlpatterns)),
    path(
        "media/<int:property_value_id>/",
        views.submission_media_download,
        name="submission_media_download",
    ),
    path(
        "adminentitiesgeojson/<int:administrative_entity_id>/",
        views.administrative_entities_geojson,
        name="administrative_entities_geojson",
    ),
    path("search/", views.submissions_search, name="submissions_search"),
    path(
        "archives/",
        views.ArchivedSubmissionListView.as_view(),
        name="archived_submission_list",
    ),
    path(
        "archives/<int:pk>/delete",
        views.ArchivedSubmissionDeleteView.as_view(),
        name="archived_submission_delete",
    ),
    path(
        "archives/<int:pk>/download",
        views.ArchivedSubmissionDownloadView.as_view(),
        name="archived_submission_download",
    ),
    path(
        "archives/bulk-download",
        views.ArchivedSubmissionBulkDownloadView.as_view(),
        name="archived_submission_bulk_download",
    ),
    path(
        "transactions/<str:merchant_reference>/change-status",
        views.ChangeTransactionStatus.as_view(),
        name="change_transaction_status",
    ),
    path(
        "transactions/confirm/<int:pk>",
        views.ConfirmTransactionCallback.as_view(),
        name="confirm_transaction",
    ),
    path(
        "transactions/fail/<int:pk>",
        views.FailTransactionCallback.as_view(),
        name="fail_transaction",
    ),
    path(
        "payment/<int:pk>",
        views.SubmissionPaymentRedirect.as_view(),
        name="submission_payment_redirect",
    ),
]
