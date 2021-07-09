# TODO split this file into multiple files
import re
import urllib.parse
import uuid
from datetime import date

from django.conf import settings
from django.contrib.auth.models import Permission
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from permits import models, services

from . import factories
from .utils import LoggedInSecretariatMixin, LoggedInUserMixin, get_emails, get_parser


def to_works_objects_dict(works_object_types):
    return {
        "works_objects-{}".format(works_object_type.works_type.pk): works_object_type.pk
        for works_object_type in works_object_types
    }


def get_permit_request_works_types_ids(permit_request):
    return list(
        permit_request.works_object_types.order_by("works_type__name")
        .values_list("works_type__pk", flat=True)
        .distinct()
    )


class PermitRequestTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.works_types = factories.WorksTypeFactory.create_batch(2)
        self.works_objects = factories.WorksObjectFactory.create_batch(2)

        models.WorksObjectType.objects.create(
            works_type=self.works_types[0],
            works_object=self.works_objects[0],
            is_public=True,
        )
        models.WorksObjectType.objects.create(
            works_type=self.works_types[1],
            works_object=self.works_objects[1],
            is_public=True,
        )
        self.geotime_step_formset_data = {
            "form-TOTAL_FORMS": ["1"],
            "form-INITIAL_FORMS": ["0"],
            "form-MIN_NUM_FORMS": ["0"],
        }

    def test_types_step_submit_redirects_to_objects_with_types_qs(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        permit_request.administrative_entity.works_object_types.set(
            models.WorksObjectType.objects.all()
        )

        response = self.client.post(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={"types": [self.works_types[0].pk, self.works_types[1].pk]},
        )

        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": permit_request.pk},
            )
            + "?types={}&types={}".format(
                self.works_types[0].pk, self.works_types[1].pk
            ),
        )

    def test_objects_step_without_qs_redirects_to_types_step(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        permit_request.administrative_entity.works_object_types.set(
            models.WorksObjectType.objects.all()
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

    def test_objects_step_submit_saves_selected_object_types(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        # Create another works object type so that the works object step is not skipped
        factories.WorksObjectTypeFactory(works_type=self.works_types[0])

        works_object_type = models.WorksObjectType.objects.first()
        permit_request.administrative_entity.works_object_types.set(
            models.WorksObjectType.objects.all()
        )
        self.client.post(
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": permit_request.pk},
            )
            + "?types={}".format(self.works_types[0].pk),
            data={
                "works_objects-{}".format(self.works_types[0].pk): works_object_type.pk
            },
        )

        self.assertEqual(
            models.PermitRequest.objects.filter(
                works_object_types=works_object_type
            ).count(),
            1,
        )

    def test_non_required_properties_can_be_left_blank(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=permit_request
        )
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactory()
        prop.works_object_types.set(permit_request.works_object_types.all())

        response = self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

    def test_documents_step_filetype_allows_jpg(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=permit_request
        )
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactoryTypeFile()
        prop.works_object_types.set(permit_request.works_object_types.all())

        with open("permits/tests/files/real_jpg.jpg", "rb") as file:
            response = self.client.post(
                reverse(
                    "permits:permit_request_appendices",
                    kwargs={"permit_request_id": permit_request.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        prop.works_object_types.last().pk, prop.pk
                    ): file
                },
            )

        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_submit",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

    def test_documents_step_filetype_allows_png(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=permit_request
        )
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactoryTypeFile()
        prop.works_object_types.set(permit_request.works_object_types.all())

        with open("permits/tests/files/real_png.png", "rb") as file:
            response = self.client.post(
                reverse(
                    "permits:permit_request_appendices",
                    kwargs={"permit_request_id": permit_request.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        prop.works_object_types.last().pk, prop.pk
                    ): file
                },
            )

        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_submit",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

    def test_documents_step_filetype_allows_pdf(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=permit_request
        )
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactoryTypeFile()
        prop.works_object_types.set(permit_request.works_object_types.all())

        with open("permits/tests/files/real_pdf.pdf", "rb") as file:
            response = self.client.post(
                reverse(
                    "permits:permit_request_appendices",
                    kwargs={"permit_request_id": permit_request.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        prop.works_object_types.last().pk, prop.pk
                    ): file
                },
            )

        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_submit",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

    def test_documents_step_filetype_reject_unknow_type_for_filetype(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=permit_request
        )
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactoryTypeFile()
        prop.works_object_types.set(permit_request.works_object_types.all())

        with open("permits/tests/files/unknow_type_for_filetype.txt", "rb") as file:
            response = self.client.post(
                reverse(
                    "permits:permit_request_appendices",
                    kwargs={"permit_request_id": permit_request.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        prop.works_object_types.last().pk, prop.pk
                    ): file
                },
            )

        content = response.content.decode()

        expected = "<div class='invalid-feedback'>{error_msg}</div>".format(
            error_msg="Le type de unknow_type_for_filetype.txt n'est pas supporté, assurez-vous que votre fichier soit du bon type",
        )
        self.assertInHTML(expected, content)

    def test_documents_step_filetype_reject_not_allowed_extension(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=permit_request
        )
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactoryTypeFile()
        prop.works_object_types.set(permit_request.works_object_types.all())

        with open("permits/tests/files/not_allowed_docx.docx", "rb") as file:
            response = self.client.post(
                reverse(
                    "permits:permit_request_appendices",
                    kwargs={"permit_request_id": permit_request.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        prop.works_object_types.last().pk, prop.pk
                    ): file
                },
            )

        content = response.content.decode()

        expected = "<div class='invalid-feedback'>{error_msg}</div>".format(
            error_msg="not_allowed_docx.docx n'est pas du bon type",
        )
        self.assertInHTML(expected, content)

    def test_documents_step_filetype_reject_fake_jpg_with_not_allowed_extension(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=permit_request
        )
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactoryTypeFile()
        prop.works_object_types.set(permit_request.works_object_types.all())

        with open("permits/tests/files/not_allowed_bmp_as_jpg.jpg", "rb") as file:
            response = self.client.post(
                reverse(
                    "permits:permit_request_appendices",
                    kwargs={"permit_request_id": permit_request.pk},
                ),
                data={
                    "appendices-{}_{}".format(
                        prop.works_object_types.last().pk, prop.pk
                    ): file
                },
            )

        content = response.content.decode()

        expected = "<div class='invalid-feedback'>{error_msg}</div>".format(
            error_msg="not_allowed_bmp_as_jpg.jpg n'est pas du bon type",
        )
        self.assertInHTML(expected, content)

    def test_user_can_only_see_own_requests(self):
        permit_request = factories.PermitRequestFactory(
            author=factories.UserFactory().permitauthor
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_edit_non_draft_request(self):
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

    def test_submit_permit_request_sends_email_to_secretariat(self):
        # Create a secretariat user Yverdon (the one that will get the notification)
        group = factories.SecretariatGroupFactory()
        factories.SecretariatUserFactory(email="secretariat@yverdon.ch", groups=[group])
        # This one should not receive the notification
        factories.SecretariatUserFactory(email="secretariat@lausanne.ch")

        permit_request = factories.PermitRequestGeoTimeFactory(
            permit_request=factories.PermitRequestFactory(
                administrative_entity=group.permitdepartment.administrative_entity,
                author=self.user.permitauthor,
                status=models.PermitRequest.STATUS_DRAFT,
            )
        ).permit_request
        self.client.post(
            reverse(
                "permits:permit_request_submit",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        emails = get_emails("Nouvelle demande")

        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0].to, ["secretariat@yverdon.ch"])

    def test_missing_mandatory_date_property_gives_invalid_feedback(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory(permit_request=permit_request)
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactory(
            input_type=models.WorksObjectProperty.INPUT_TYPE_DATE, is_mandatory=True
        )
        prop.works_object_types.set(permit_request.works_object_types.all())

        data = {
            "properties-{}_{}".format(works_object_type.pk, prop.pk): ""
            for works_object_type in permit_request.works_object_types.all()
        }

        response = self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=data,
        )
        parser = get_parser(response.content)
        self.assertEqual(len(parser.select(".invalid-feedback")), 1)

    def test_works_object_automatically_set_when_only_one_works_object(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object = factories.WorksObjectFactory()
        permit_request.administrative_entity.works_object_types.set(
            factories.WorksObjectTypeFactory.create_batch(2, works_object=works_object)
        )
        works_type_id = permit_request.administrative_entity.works_object_types.values_list(
            "works_type_id", flat=True
        ).first()

        self.client.post(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={"types": [works_type_id]},
        )

        permit_request.refresh_from_db()
        works_object_types = permit_request.works_object_types.all()

        self.assertEqual(
            len(works_object_types),
            1,
            "Permit request should have one works object type set",
        )
        self.assertEqual(works_object_types[0].works_object, works_object)
        self.assertEqual(works_object_types[0].works_type_id, works_type_id)

    def test_works_type_automatically_set_when_only_one_works_object(self):
        works_type = factories.WorksTypeFactory()
        administrative_entity = factories.PermitAdministrativeEntityFactory()
        administrative_entity.works_object_types.set(
            factories.WorksObjectTypeFactory.create_batch(2, works_type=works_type)
        )

        response = self.client.post(
            reverse("permits:permit_request_select_administrative_entity",),
            data={"administrative_entity": administrative_entity.pk},
        )

        permit_request = models.PermitRequest.objects.get()

        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": permit_request.pk},
            )
            + f"?types={works_type.pk}",
        )

    def test_geotime_step_only_date_fields_appear_when_only_date_is_required(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeWithoutGeometryFactory(
            needs_date=True,
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select('input[name="form-0-starts_at"]')), 1,
        )
        self.assertEqual(len(parser.select('input[name="form-0-ends_at"]')), 1)

        self.assertEqual(
            len(parser.select('textarea[name="form-0-geom"]')), 0,
        )

    def test_geotime_step_date_fields_cannot_be_empty_when_date_is_required(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeWithoutGeometryFactory(
            needs_date=True,
        )
        permit_request.works_object_types.set([works_object_type])
        self.geotime_step_formset_data.update(
            {"form-0-starts_at": [""], "form-0-ends_at": [""]}
        )
        response = self.client.post(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=self.geotime_step_formset_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormsetError(
            response, "formset", 0, "starts_at", "Ce champ est obligatoire.",
        )
        self.assertFormsetError(
            response, "formset", 0, "ends_at", "Ce champ est obligatoire.",
        )

    def test_geotime_step_date_fields_ends_at_must_not_be_before_starts_at(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeWithoutGeometryFactory(
            needs_date=True,
        )
        permit_request.works_object_types.set([works_object_type])
        self.geotime_step_formset_data.update(
            {
                "form-0-starts_at": ["2021-04-17 14:05:00+02:00"],
                "form-0-ends_at": ["2021-04-16 14:05:00+02:00"],
            }
        )

        response = self.client.post(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=self.geotime_step_formset_data,
        )

        self.assertEqual(response.status_code, 200)
        self.assertFormsetError(
            response,
            "formset",
            0,
            None,
            "La date de fin doit être postérieure à la date de début.",
        )

    def test_geotime_step_only_geom_fields_appear_when_only_geom_is_required(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeFactory(
            has_geometry_point=True,
            has_geometry_line=True,
            has_geometry_polygon=True,
            needs_date=False,
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select('textarea[name="form-0-geom"]')), 1,
        )

        self.assertEqual(
            len(parser.select('input[name="form-0-starts_at"]')), 0,
        )
        self.assertEqual(len(parser.select('input[name="form-0-ends_at"]')), 0)

    def test_geotime_step_date_and_geom_fields_appear_when_both_required(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeFactory(
            has_geometry_point=True,
            has_geometry_line=True,
            has_geometry_polygon=True,
            needs_date=True,
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select('input[name="form-0-starts_at"]')), 1,
        )
        self.assertEqual(len(parser.select('input[name="form-0-ends_at"]')), 1)
        self.assertEqual(
            len(parser.select('textarea[name="form-0-geom"]')), 1,
        )

    def test_geotime_step_only_point_geom_field_appear_when_only_point_geom_type_is_required(
        self,
    ):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeFactory(
            has_geometry_point=True,
            has_geometry_line=False,
            has_geometry_polygon=False,
            needs_date=False,
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPoint"]'
                )
            ),
            1,
        )

        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiLineString"]'
                )
            ),
            0,
        )
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPolygon"]'
                )
            ),
            0,
        )

    def test_geotime_step_only_line_geom_field_appear_when_only_line_geom_type_is_required(
        self,
    ):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeFactory(
            has_geometry_point=False,
            has_geometry_line=True,
            has_geometry_polygon=False,
            needs_date=False,
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPoint"]'
                )
            ),
            0,
        )

        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiLineString"]'
                )
            ),
            1,
        )
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPolygon"]'
                )
            ),
            0,
        )

    def test_geotime_step_only_polygon_geom_field_appear_when_only_polygon_geom_type_is_required(
        self,
    ):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeFactory(
            has_geometry_point=False,
            has_geometry_line=False,
            has_geometry_polygon=True,
            needs_date=False,
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPoint"]'
                )
            ),
            0,
        )

        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiLineString"]'
                )
            ),
            0,
        )
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPolygon"]'
                )
            ),
            1,
        )

    def test_geotime_step_only_two_geom_field_appear_when_only_two_geom_type_are_required(
        self,
    ):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeFactory(
            has_geometry_point=True,
            has_geometry_line=False,
            has_geometry_polygon=True,
            needs_date=False,
        )
        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPoint"]'
                )
            ),
            1,
        )

        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiLineString"]'
                )
            ),
            0,
        )
        self.assertEqual(
            len(
                parser.select(
                    '#geometry-widget-id_form-0-geom input[data-interaction-type="MultiPolygon"]'
                )
            ),
            1,
        )

    def test_summary_and_send_step_has_multiple_directive_fields_when_request_have_multiple_works_object_type(
        self,
    ):
        group = factories.SecretariatGroupFactory()
        first_works_object_type = factories.WorksObjectTypeFactory(
            directive=SimpleUploadedFile("file.pdf", "contents".encode()),
            directive_description="First directive description for a test",
            additional_information="First additional information for a test",
        )
        second_works_object_type = factories.WorksObjectTypeFactory(
            directive=SimpleUploadedFile("file.pdf", "contents".encode()),
            directive_description="Second directive description for a test",
            additional_information="Second additional information for a test",
        )

        permit_request = factories.PermitRequestGeoTimeFactory(
            permit_request=factories.PermitRequestFactory(
                administrative_entity=group.permitdepartment.administrative_entity,
                author=self.user.permitauthor,
                status=models.PermitRequest.STATUS_DRAFT,
            )
        ).permit_request

        permit_request.works_object_types.set(
            [first_works_object_type, second_works_object_type]
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_submit",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        parser = get_parser(response.content)

        self.assertEqual(
            len(parser.select("#legal-infos span.directive_description")), 2,
        )

        self.assertEqual(
            len(parser.select("#legal-infos a.directive_file")), 2,
        )

        self.assertEqual(
            len(parser.select("#legal-infos span.additional_information")), 2,
        )

    def test_administrative_entity_is_filtered_by_tag(self):
        administrative_entities = [
            factories.PermitAdministrativeEntityFactory(tags=[tag])
            for tag in ["first", "second", "third"]
        ]
        works_object_types = models.WorksObjectType.objects.all()

        for administrative_entity in administrative_entities:
            administrative_entity.works_object_types.set(works_object_types)

        response = self.client.get(
            reverse("permits:permit_request_select_administrative_entity"),
            {"filter": "first"},
        )

        parser = get_parser(response.content)
        element_parsed = parser.select(".form-check-label")

        content = response.content.decode()
        # Check that selected item is there
        self.assertEqual(1, len(element_parsed))
        # Check that filtered items are NOT there
        self.assertNotContains(response, administrative_entities[1].name)
        self.assertNotContains(response, administrative_entities[2].name)
        self.assertInHTML(administrative_entities[0].name, content)

    def test_wrong_administrative_entity_tag_return_all_administratives_entities(self):
        administrative_entities = [
            factories.PermitAdministrativeEntityFactory(tags=[tag])
            for tag in ["first", "second", "third"]
        ]
        works_object_types = models.WorksObjectType.objects.all()

        for administrative_entity in administrative_entities:
            administrative_entity.works_object_types.set(works_object_types)

        response = self.client.get(
            reverse("permits:permit_request_select_administrative_entity"),
            {"filter": "wrongtag"},
        )

        parser = get_parser(response.content)
        element_parsed = parser.select(".form-check-label")

        content = response.content.decode()

        self.assertEqual(3, len(element_parsed))
        self.assertInHTML(administrative_entities[0].name, content)
        self.assertInHTML(administrative_entities[1].name, content)
        self.assertInHTML(administrative_entities[2].name, content)

    def test_multiple_administrative_entity_tags_return_multiple_administratives_entities(
        self,
    ):
        administrative_entities = [
            factories.PermitAdministrativeEntityFactory(tags=[tag])
            for tag in ["first", "second", "third"]
        ]
        works_object_types = models.WorksObjectType.objects.all()

        for administrative_entity in administrative_entities:
            administrative_entity.works_object_types.set(works_object_types)

        response = self.client.get(
            reverse("permits:permit_request_select_administrative_entity"),
            {"filter": ["first", "second"]},
        )

        parser = get_parser(response.content)
        element_parsed = parser.select(".form-check-label")

        content = response.content.decode()

        self.assertEqual(2, len(element_parsed))
        self.assertInHTML(administrative_entities[0].name, content)
        self.assertInHTML(administrative_entities[1].name, content)


class PermitRequestActorsTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()

        self.test_formset_data = {
            "form-TOTAL_FORMS": ["1"],
            "form-INITIAL_FORMS": ["0"],
            "form-MIN_NUM_FORMS": ["0"],
            "form-MAX_NUM_FORMS": ["1000"],
            "creditor_type": [""],
            "form-0-actor_type": "",
            "form-0-first_name": ["John"],
            "form-0-last_name": ["Doe"],
            "form-0-phone": ["000 000 00 00"],
            "form-0-email": ["john@doe.com"],
            "form-0-address": ["Main street 1"],
            "form-0-zipcode": ["2000"],
            "form-0-city": ["City"],
            "form-0-company_name": [""],
            "form-0-vat_number": [""],
            "form-0-id": [""],
        }

    def test_permitrequestactor_creates(self):
        works_object_type = factories.WorksObjectTypeFactory()
        works_type = works_object_type.works_type

        actor_required = factories.PermitActorTypeFactory(
            is_mandatory=True, works_type=works_type
        )

        self.test_formset_data["form-0-actor_type"] = actor_required.type

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_DRAFT
        )

        permit_request.administrative_entity.works_object_types.set([works_object_type])
        permit_request.works_object_types.set([works_object_type])
        prop = factories.WorksObjectPropertyFactory()
        prop.works_object_types.set([works_object_type])

        self.client.post(
            reverse(
                "permits:permit_request_actors",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=self.test_formset_data,
        )

        actors = list(permit_request.actors.all())
        self.assertEqual(len(actors), 1, "Expected 1 actor created")
        self.assertEqual(actors[0].first_name, "John")

    def test_permitrequestactor_required_cannot_have_empty_field(self):
        works_object_type = factories.WorksObjectTypeFactory()
        works_type = works_object_type.works_type

        actor_required = factories.PermitActorTypeFactory(
            is_mandatory=True, works_type=works_type
        )

        self.test_formset_data["form-0-actor_type"] = actor_required.type

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_DRAFT
        )

        permit_request.administrative_entity.works_object_types.set([works_object_type])
        permit_request.works_object_types.set([works_object_type])
        prop = factories.WorksObjectPropertyFactory()
        prop.works_object_types.set([works_object_type])

        self.test_formset_data["form-0-last_name"] = ""

        response = self.client.post(
            reverse(
                "permits:permit_request_actors",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
            data=self.test_formset_data,
        )

        permit_request.refresh_from_db()
        # Check that no actor was saved for this permit
        self.assertEqual(permit_request.actors.count(), 0)
        # Check that if form not valid, it does not redirect
        self.assertEqual(response.status_code, 200)

    def test_permitrequestactor_creditor_field_is_hidden_if_wot_is_not_paid(self):
        works_object_type = factories.WorksObjectTypeFactory(requires_payment=False)
        works_type = works_object_type.works_type

        factories.PermitActorTypeFactory(is_mandatory=True, works_type=works_type)

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_DRAFT
        )

        permit_request.works_object_types.set([works_object_type])

        response = self.client.get(
            reverse(
                "permits:permit_request_actors",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
        )

        parser = get_parser(response.content)

        self.assertEqual(
            len(parser.findAll(text=re.compile("Renseignez les contacts"))), 1
        )
        self.assertIsNone(parser.find(id="id_creditor_type"))
        self.assertEqual(
            len(
                parser.findAll(
                    text=re.compile(
                        "Adresse de facturation si différente de celle de l'auteur"
                    )
                )
            ),
            0,
        )

    def test_permitrequestactor_creditor_field_is_shown_if_at_least_one_wot_requires_payment(
        self,
    ):

        free_works_object_types = factories.WorksObjectTypeFactory.create_batch(
            2, requires_payment=False
        )
        paid_works_object_type = factories.WorksObjectTypeFactory(requires_payment=True)
        works_types = [wt.works_type for wt in free_works_object_types] + [
            paid_works_object_type.works_type
        ]

        for wt in works_types:
            factories.PermitActorTypeFactory(is_mandatory=True, works_type=wt)

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_DRAFT
        )

        permit_request.works_object_types.set(
            free_works_object_types + [paid_works_object_type]
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_actors",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
        )

        parser = get_parser(response.content)

        self.assertEqual(
            len(parser.findAll(text=re.compile("Renseignez les contacts"))), 1
        )
        self.assertGreaterEqual(len(parser.find(id="id_creditor_type")), 1)
        self.assertEqual(
            len(
                parser.findAll(
                    text=re.compile(
                        "Adresse de facturation si différente de celle de l'auteur"
                    )
                )
            ),
            1,
        )


class PermitRequestUpdateTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor
        )
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=self.permit_request
        )
        self.permit_request.administrative_entity.works_object_types.set(
            self.permit_request.works_object_types.all()
        )

    def test_types_step_submit_shows_new_objects(self):
        new_works_object_type = factories.WorksObjectTypeFactory()

        new_works_object_type.administrative_entities.set(
            [self.permit_request.administrative_entity]
        )

        response = self.client.post(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            follow=True,
            data={
                "types": get_permit_request_works_types_ids(self.permit_request)
                + [new_works_object_type.works_type.pk]
            },
        )

        self.assertContains(response, new_works_object_type.works_type)

    def test_types_step_submit_removes_deselected_types_from_permit_request(self):
        works_object_type_id = get_permit_request_works_types_ids(self.permit_request)[
            0
        ]

        self.client.post(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data={"types": works_object_type_id},
        )

        self.permit_request.refresh_from_db()

        self.assertEqual(models.PermitRequest.objects.count(), 1)
        self.assertEqual(
            get_permit_request_works_types_ids(self.permit_request),
            [works_object_type_id],
        )

    def test_objects_step_submit_updates_permit_request(self):
        new_works_object_type = factories.WorksObjectTypeFactory()
        self.permit_request.administrative_entity.works_object_types.add(
            new_works_object_type
        )
        current_works_object_types = list(self.permit_request.works_object_types.all())
        current_works_object_types_dict = to_works_objects_dict(
            current_works_object_types
        )
        new_works_object_types_dict = to_works_objects_dict([new_works_object_type])
        works_types_ids = get_permit_request_works_types_ids(self.permit_request) + [
            new_works_object_type.works_type.pk
        ]
        types_param = urllib.parse.urlencode({"types": works_types_ids}, doseq=True)

        self.client.post(
            (
                reverse(
                    "permits:permit_request_select_objects",
                    kwargs={"permit_request_id": self.permit_request.pk},
                )
                + "?"
                + types_param
            ),
            data={**current_works_object_types_dict, **new_works_object_types_dict},
        )

        self.permit_request.refresh_from_db()

        self.assertEqual(models.PermitRequest.objects.count(), 1)
        self.assertEqual(
            set(self.permit_request.works_object_types.all()),
            set(current_works_object_types + [new_works_object_type]),
        )

    def test_properties_step_submit_updates_permit_request(self):
        new_prop = factories.WorksObjectPropertyFactory()
        new_prop.works_object_types.set(self.permit_request.works_object_types.all())
        data = {
            "properties-{}_{}".format(
                works_object_type.pk, new_prop.pk
            ): "value-{}".format(works_object_type.pk)
            for works_object_type in self.permit_request.works_object_types.all()
        }
        self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data=data,
        )

        self.assertEqual(
            set(
                item["val"]
                for item in services.get_properties_values(
                    self.permit_request
                ).values_list("value", flat=True)
            ),
            set(data.values()),
        )

    def test_missing_mandatory_address_property_gives_invalid_feedback(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory(permit_request=permit_request)
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        prop = factories.WorksObjectPropertyFactoryTypeAddress(
            input_type=models.WorksObjectProperty.INPUT_TYPE_ADDRESS, is_mandatory=True
        )
        prop.works_object_types.set(permit_request.works_object_types.all())

        data = {
            "properties-{}_{}".format(works_object_type.pk, prop.pk): ""
            for works_object_type in permit_request.works_object_types.all()
        }

        response = self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=data,
        )
        parser = get_parser(response.content)
        self.assertEqual(1, len(parser.select(".invalid-feedback")))

    def test_properties_step_submit_updates_permit_request_with_address(self):
        address_prop = factories.WorksObjectPropertyFactoryTypeAddress(
            input_type=models.WorksObjectProperty.INPUT_TYPE_ADDRESS
        )
        address_prop.works_object_types.set(
            self.permit_request.works_object_types.all()
        )
        works_object_type = self.permit_request.works_object_types.first()
        data = {
            f"properties-{works_object_type.pk}_{address_prop.pk}": "Hôtel Martinez, Cannes"
        }
        self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data=data,
        )

        self.permit_request.refresh_from_db()
        prop_val = services.get_properties_values(self.permit_request).get(
            property__input_type=models.WorksObjectProperty.INPUT_TYPE_ADDRESS
        )
        self.assertEqual(prop_val.value, {"val": "Hôtel Martinez, Cannes"})

    def test_properties_step_submit_updates_permit_request_with_date(self):

        date_prop = factories.WorksObjectPropertyFactory(
            input_type=models.WorksObjectProperty.INPUT_TYPE_DATE, name="datum"
        )
        today = date.today()
        works_object_type = self.permit_request.works_object_types.first()
        date_prop.works_object_types.set([works_object_type])
        data = {
            f"properties-{works_object_type.pk}_{date_prop.pk}": today.strftime(
                settings.DATE_INPUT_FORMAT
            )
        }
        self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data=data,
        )

        prop_val = services.get_properties_values(self.permit_request).get(
            property__name="datum"
        )
        self.assertEqual(
            prop_val.value, {"val": today.isoformat()},
        )
        self.assertEqual(
            prop_val.property.input_type, models.WorksObjectProperty.INPUT_TYPE_DATE,
        )


class PermitRequestPrefillTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor
        )
        factories.WorksObjectTypeChoiceFactory.create_batch(
            3, permit_request=self.permit_request
        )
        self.permit_request.administrative_entity.works_object_types.set(
            self.permit_request.works_object_types.all()
        )

    def test_types_step_preselects_types_for_existing_permit_request(self):
        response = self.client.get(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )
        content = response.content.decode()

        for i, works_type_id in enumerate(
            get_permit_request_works_types_ids(self.permit_request)
        ):
            expected = (
                '<input checked="" class="form-check-input" id="id_types_{i}" name="types" title=""'
                '  type="checkbox" value="{value}"/>'
            ).format(value=works_type_id, i=i)
            self.assertInHTML(expected, content)

    def test_objects_step_preselects_objects_for_existing_permit_request(self):
        response = self.client.get(
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )
        content = response.content.decode()

        for works_object_type in self.permit_request.works_object_types.all():
            expected = (
                '<input checked="" class="form-check-input" id="id_works_objects-{id}_0"'
                ' name="works_objects-{id}" title="" type="checkbox" value="{value}"/>'
            ).format(id=works_object_type.works_type.pk, value=works_object_type.pk)
            self.assertInHTML(expected, content)

    def test_properties_step_prefills_properties_for_existing_permit_request(self):
        works_object_type_choice = services.get_works_object_type_choices(
            self.permit_request
        ).first()
        prop = factories.WorksObjectPropertyFactory()
        prop.works_object_types.add(works_object_type_choice.works_object_type)
        prop_value = factories.WorksObjectPropertyValueFactory(
            works_object_type_choice=works_object_type_choice, property=prop
        )
        response = self.client.get(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )
        content = response.content.decode()
        expected = '<textarea name="properties-{obj_type_id}_{prop_id}" cols="40" rows="1" placeholder="ex: {placeholder}" class="form-control" title="{help_text}" id="id_properties-{obj_type_id}_{prop_id}">{value}'.format(
            obj_type_id=works_object_type_choice.works_object_type.pk,
            prop_id=prop.pk,
            prop_name=prop.name,
            value=prop_value.value["val"],
            placeholder=prop.placeholder,
            help_text=prop.help_text,
        )

        expected_help_text = '<small class="form-text text-muted">{help_text}</small>'.format(
            help_text=prop.help_text,
        )

        self.assertInHTML(expected, content)
        self.assertInHTML(expected_help_text, content)

    def test_properties_step_order_properties_for_existing_permit_request(self):

        works_object_type_choice = services.get_works_object_type_choices(
            self.permit_request
        ).first()

        prop_1 = factories.WorksObjectPropertyFactory(order=10, name=str(uuid.uuid4()))
        prop_2 = factories.WorksObjectPropertyFactory(order=2, name=str(uuid.uuid4()))
        prop_1.works_object_types.add(works_object_type_choice.works_object_type)
        prop_2.works_object_types.add(works_object_type_choice.works_object_type)

        response = self.client.get(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )
        content = response.content.decode()
        position_1 = content.find(prop_1.name)
        position_2 = content.find(prop_2.name)
        self.assertGreater(position_1, position_2)


class PermitRequestAmendmentTestCase(LoggedInSecretariatMixin, TestCase):
    def test_non_secretariat_user_cannot_amend_request(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=user.permitauthor,
        )
        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "status": models.PermitRequest.STATUS_PROCESSING,
                "action": models.ACTION_AMEND,
            },
        )

        permit_request.refresh_from_db()
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            permit_request.status, models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION
        )

    def test_secretariat_can_amend_request_with_custom_property_field_and_delete_property_value(
        self,
    ):
        props_quantity = 3
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )
        works_object_type_choice = factories.WorksObjectTypeChoiceFactory(
            permit_request=permit_request
        )

        props = factories.PermitRequestAmendPropertyFactory.create_batch(props_quantity)

        data = {
            "action": models.ACTION_AMEND,
            "status": models.PermitRequest.STATUS_PROCESSING,
        }

        works_object_types_pk = permit_request.works_object_types.first().pk
        for prop in props:
            prop.works_object_types.set(permit_request.works_object_types.all())
            factories.PermitRequestAmendPropertyValueFactory(
                property=prop, works_object_type_choice=works_object_type_choice,
            )
            data[
                f"{works_object_types_pk}_{prop.pk}"
            ] = "I am a new property value, I am alive!"

        # The delete latter property value by setting it to an empty string
        data[f"{works_object_types_pk}_{props[-1].pk}"] = ""

        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=data,
        )

        new_properties_values_qs = models.PermitRequestAmendPropertyValue.objects.values_list(
            "value", flat=True
        )
        self.assertEqual(len(new_properties_values_qs), props_quantity - 1)
        self.assertIn(
            "I am a new property value, I am alive!", new_properties_values_qs,
        )

    def test_author_cannot_see_private_secretariat_amend_property(self,):

        props_quantity = 3
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )
        works_object_type_choice = factories.WorksObjectTypeChoiceFactory(
            permit_request=permit_request
        )

        props_public = factories.PermitRequestAmendPropertyFactory.create_batch(
            props_quantity, is_visible_by_author=True
        )
        props_private = factories.PermitRequestAmendPropertyFactory.create_batch(
            props_quantity, is_visible_by_author=False
        )

        props = props_public + props_private

        self.client.login(
            username=permit_request.author.user.username, password="password"
        )
        data = {
            "action": models.ACTION_AMEND,
            "status": models.PermitRequest.STATUS_PROCESSING,
        }
        works_object_types_pk = permit_request.works_object_types.first().pk
        for prop in props:
            prop.works_object_types.set(permit_request.works_object_types.all())
            factories.PermitRequestAmendPropertyValueFactory(
                property=prop, works_object_type_choice=works_object_type_choice,
            )
            data[
                f"{works_object_types_pk}_{prop.pk}"
            ] = "I am a new property value, I am alive!"

        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

        parser = get_parser(response.content)
        # check that 3 fields are visible by author and 3 are hidden
        self.assertEqual(len(parser.select(".amend-property")), 3)

    def test_secretariat_can_see_submitted_requests(self):
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.get(reverse("permits:permit_requests_list"))

        self.assertEqual(list(response.context["permitrequest_list"]), [permit_request])

    def test_ask_for_supplements_shows_specific_message(self):
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "status": models.PermitRequest.STATUS_AWAITING_SUPPLEMENT,
                "action": models.ACTION_AMEND,
            },
            follow=True,
        )
        permit_request.refresh_from_db()
        self.assertEqual(
            permit_request.status, models.PermitRequest.STATUS_AWAITING_SUPPLEMENT
        )
        self.assertContains(response, "compléments")

    def test_secretariat_cannot_amend_permit_request_with_validation_requested(self):
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "status": models.PermitRequest.STATUS_AWAITING_SUPPLEMENT,
                "action": models.ACTION_AMEND,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_secretariat_can_see_print_buttons_and_directives(self):
        first_works_object_type = factories.WorksObjectTypeFactory(
            directive=SimpleUploadedFile("file.pdf", "contents".encode()),
            directive_description="First directive description for a test",
            additional_information="First additional information for a test",
        )
        second_works_object_type = factories.WorksObjectTypeFactory(
            directive=SimpleUploadedFile("file.pdf", "contents".encode()),
            directive_description="Second directive description for a test",
            additional_information="Second additional information for a test",
        )
        factories.QgisProjectFactory(
            qgis_project_file=SimpleUploadedFile("template.qgs", "contents".encode()),
            description="Print Template 1",
            works_object_type=first_works_object_type,
        )
        factories.QgisProjectFactory(
            qgis_project_file=SimpleUploadedFile("template.qgs", "contents".encode()),
            description="Print Template 2",
            works_object_type=second_works_object_type,
        )

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )

        permit_request.works_object_types.set(
            [first_works_object_type, second_works_object_type]
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".tab-pane#print button")), 2,
        )
        self.assertEqual(
            len(parser.select(".tab-pane#print span.directive_description")), 2,
        )

    def test_secretariat_cannot_see_print_buttons_and_directives_if_not_configured(
        self,
    ):
        works_object_types = factories.WorksObjectTypeFactory.create_batch(2)

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )

        permit_request.works_object_types.set(works_object_types)

        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".tab-pane#print button")), 0,
        )
        self.assertEqual(
            len(parser.select(".tab-pane#print span.directive_description")), 0,
        )
        self.assertEqual(
            len(parser.select(".tab-pane#print span.no_directive")), 1,
        )
        self.assertEqual(
            len(parser.select(".tab-pane#print span.no_print_template")), 1,
        )


class PermitRequestValidationRequestTestcase(LoggedInSecretariatMixin, TestCase):
    def test_secretariat_can_request_validation(self):
        validator_groups = factories.ValidatorGroupFactory.create_batch(
            2, department__administrative_entity=self.administrative_entity
        )
        validator_departments = [
            group.permitdepartment.pk for group in validator_groups
        ]

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "departments": validator_departments,
                "action": models.ACTION_REQUEST_VALIDATION,
            },
        )

        permit_request.refresh_from_db()

        self.assertEqual(
            permit_request.status, models.PermitRequest.STATUS_AWAITING_VALIDATION
        )
        self.assertEqual(
            list(permit_request.validations.values_list("department", flat=True)),
            validator_departments,
        )

    def test_secretariat_cannot_request_validation_for_already_validated_permit_request(
        self,
    ):
        validator_group = factories.ValidatorGroupFactory(
            department__administrative_entity=self.administrative_entity
        )

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "departments": [validator_group.permitdepartment.pk],
                "action": models.ACTION_REQUEST_VALIDATION,
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_default_departments_are_checked(self):
        default_validator_groups = factories.ValidatorGroupFactory.create_batch(
            2,
            department__administrative_entity=self.administrative_entity,
            department__is_default_validator=True,
        )
        non_default_validator_group = factories.ValidatorGroupFactory(
            department__administrative_entity=self.administrative_entity
        )

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_PROCESSING,
            administrative_entity=self.administrative_entity,
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

        parser = get_parser(response.content)
        inputs = {
            int(input_["value"]): input_.get("checked") is not None
            for input_ in parser.select('input[name="departments"]')
        }

        self.assertDictEqual(
            inputs,
            {
                **{group.pk: True for group in default_validator_groups},
                **{non_default_validator_group.pk: False},
            },
        )

    def test_validation_request_sends_mail_to_selected_validators(self):
        validator_groups = factories.ValidatorGroupFactory.create_batch(
            2, department__administrative_entity=self.administrative_entity
        )
        validator_user = factories.ValidatorUserFactory(groups=[validator_groups[0]])
        factories.ValidatorUserFactory(groups=[validator_groups[1]])

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "departments": [validator_groups[0].permitdepartment.pk],
                "action": models.ACTION_REQUEST_VALIDATION,
            },
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [validator_user.permitauthor.user.email])


class PermitRequestValidationTestcase(TestCase):
    def test_validator_can_see_assigned_permit_requests(self):
        validation = factories.PermitRequestValidationFactory()
        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

        self.client.login(username=validator.username, password="password")

        response = self.client.get(reverse("permits:permit_requests_list"))

        self.assertEqual(
            list(response.context["permitrequest_list"]), [validation.permit_request]
        )

    def test_validator_can_validate_assigned_permit_requests(self):
        validation = factories.PermitRequestValidationFactory()
        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

        self.client.login(username=validator.username, password="password")

        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={
                "action": models.ACTION_VALIDATE,
                "validation_status": models.PermitRequestValidation.STATUS_APPROVED,
            },
        )

        validation.refresh_from_db()

        self.assertEqual(
            validation.validation_status, models.PermitRequestValidation.STATUS_APPROVED
        )

    def test_validator_can_validate_assigned_permit_requests_and_secretary_mail_is_sent(
        self,
    ):
        validation = factories.PermitRequestValidationFactory()
        secretary_group = factories.GroupFactory(name="Secrétariat")
        department = factories.PermitDepartmentFactory(group=secretary_group)
        factories.SecretariatUserFactory(groups=[secretary_group])
        validation.permit_request.administrative_entity.departments.set([department])

        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

        self.client.login(username=validator.username, password="password")

        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={
                "action": models.ACTION_VALIDATE,
                "validation_status": models.PermitRequestValidation.STATUS_APPROVED,
            },
        )

        validation.refresh_from_db()

        self.assertEqual(
            validation.validation_status, models.PermitRequestValidation.STATUS_APPROVED
        )

    def test_validator_cannot_validate_non_assigned_permit_requests(self):
        validation = factories.PermitRequestValidationFactory()
        factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )
        validator = factories.ValidatorUserFactory()

        self.client.login(username=validator.username, password="password")

        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={
                "action": models.ACTION_VALIDATE,
                "validation_status": models.PermitRequestValidation.STATUS_APPROVED,
            },
        )

        self.assertEqual(response.status_code, 404)

    def test_secretariat_can_send_validation_reminders(self):
        group = factories.SecretariatGroupFactory()
        administrative_entity = group.permitdepartment.administrative_entity
        secretariat = factories.SecretariatUserFactory(groups=[group])

        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=administrative_entity
        )
        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

        self.client.login(username=secretariat.username, password="password")

        self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={"action": models.ACTION_POKE,},
        )

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [validator.permitauthor.user.email])


class PermitRequestClassifyTestCase(TestCase):
    def setUp(self):
        self.secretariat_group = factories.SecretariatGroupFactory()
        self.administrative_entity = (
            self.secretariat_group.permitdepartment.administrative_entity
        )
        self.secretariat_user = factories.SecretariatUserFactory(
            groups=[self.secretariat_group]
        )

        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity
        )
        self.validator_user = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

    def test_secretariat_can_classify_permit_request(self):
        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
        )

        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.post(
            reverse(
                "permits:permit_request_approve",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={
                "validation_pdf": SimpleUploadedFile("file.pdf", "contents".encode())
            },
        )

        self.assertRedirects(response, reverse("permits:permit_requests_list"))
        validation.permit_request.refresh_from_db()
        self.assertEqual(
            validation.permit_request.status, models.PermitRequest.STATUS_APPROVED
        )

    def test_secretariat_cannot_classify_permit_request_with_pending_validations(self):
        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity
        )

        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.post(
            reverse(
                "permits:permit_request_approve",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={"validation_pdf": SimpleUploadedFile("file.pdf", "")},
        )

        self.assertEqual(response.status_code, 404)

    def test_secretariat_does_not_see_classify_form_when_pending_validations(self):
        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity
        )

        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": validation.permit_request.pk},
            )
        )

        self.assertNotContains(
            response,
            reverse(
                "permits:permit_request_approve",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
        )

    def test_user_without_permission_cannot_classify_permit_request(self):
        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
        )
        user = factories.UserFactory(actor=validation.permit_request.author)
        self.client.login(username=user.username, password="password")

        approve_url = reverse(
            "permits:permit_request_approve",
            kwargs={"permit_request_id": validation.permit_request.pk},
        )

        response = self.client.post(
            approve_url, data={"validation_pdf": SimpleUploadedFile("file.pdf", "")}
        )

        self.assertRedirects(
            response, "%s?next=%s" % (reverse(settings.LOGIN_URL), approve_url)
        )

    def test_permit_request_validation_file_accessible_to_permit_request_author(self):
        author_user = factories.UserFactory()
        permit_request = factories.PermitRequestFactory(
            validated_at=timezone.now(),
            status=models.PermitRequest.STATUS_APPROVED,
            author=author_user.permitauthor,
        )
        # This cannot be performed in the factory because we need the permit request to have an id to upload a file
        permit_request.validation_pdf = SimpleUploadedFile("file.pdf", b"contents")
        permit_request.save()

        self.client.login(username=author_user, password="password")
        response = self.client.get(permit_request.validation_pdf.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"".join(response.streaming_content), b"contents")

    def test_permit_request_validation_file_not_accessible_to_other_users(self):
        non_author_user = factories.UserFactory()
        permit_request = factories.PermitRequestFactory(
            validated_at=timezone.now(), status=models.PermitRequest.STATUS_APPROVED
        )
        # This cannot be performed in the factory because we need the permit request to have an id to upload a file
        permit_request.validation_pdf = SimpleUploadedFile("file.pdf", b"contents")
        permit_request.save()

        self.client.login(username=non_author_user, password="password")
        response = self.client.get(permit_request.validation_pdf.url)
        self.assertEqual(response.status_code, 404)

    def test_classify_sets_validation_date(self):
        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
        )

        self.client.login(username=self.secretariat_user.username, password="password")
        self.client.post(
            reverse(
                "permits:permit_request_approve",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={"validation_pdf": SimpleUploadedFile("file.pdf", b"contents")},
        )

        validation.permit_request.refresh_from_db()
        self.assertIsNotNone(validation.permit_request.validated_at)


class ApprovedPermitRequestClassifyTestCase(TestCase):
    def setUp(self):
        self.secretariat_group = factories.SecretariatGroupFactory()
        self.administrative_entity = (
            self.secretariat_group.permitdepartment.administrative_entity
        )
        self.secretariat_user = factories.SecretariatUserFactory(
            groups=[self.secretariat_group]
        )

        self.validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
        )
        self.client.login(username=self.secretariat_user.username, password="password")

    def _get_approval(self):
        response = self.client.get(
            reverse(
                "permits:permit_request_approve",
                kwargs={"permit_request_id": self.validation.permit_request.pk},
            ),
        )
        self.assertContains(response, "Approbation de la demande")
        self.assertEqual(
            self.validation.permit_request.status,
            models.PermitRequest.STATUS_AWAITING_VALIDATION,
        )
        return response

    def test_classify_permit_request_with_required_validation_doc_shows_file_field(
        self,
    ):
        wot = factories.WorksObjectTypeFactory(requires_validation_document=True)
        self.validation.permit_request.works_object_types.set([wot])
        response = self._get_approval()
        self.assertContains(response, "validation_pdf")

    def test_classify_permit_request_without_required_validation_doc_does_not_show_file_field(
        self,
    ):
        wot = factories.WorksObjectTypeFactory(requires_validation_document=False)
        self.validation.permit_request.works_object_types.set([wot])
        response = self._get_approval()
        self.assertNotContains(response, "validation_pdf")

    def test_classify_permit_request_with_any_object_requiring_validation_doc_shows_file_field(
        self,
    ):
        wot1 = factories.WorksObjectTypeFactory(requires_validation_document=True)
        wot2 = factories.WorksObjectTypeFactory(requires_validation_document=False)
        self.validation.permit_request.works_object_types.set([wot1, wot2])
        response = self._get_approval()
        self.assertContains(response, "validation_pdf")


class PrivateDemandsTestCase(LoggedInUserMixin, TestCase):
    def test_administrative_entity_step_without_public_requests_is_empty_to_standard_user(
        self,
    ):

        works_types = factories.WorksTypeFactory.create_batch(2)
        works_objects = factories.WorksObjectFactory.create_batch(2)

        administrative_entity = factories.PermitAdministrativeEntityFactory(
            name="privateEntity"
        )
        private_works_object_type = models.WorksObjectType.objects.create(
            works_type=works_types[0], works_object=works_objects[0], is_public=False,
        )
        private_works_object_type.administrative_entities.set([administrative_entity])
        response = self.client.get(
            reverse("permits:permit_request_select_administrative_entity",),
        )
        self.assertNotContains(response, "privateEntity")

    def test_administrative_entity_step_without_public_requests_is_visible_to_user_with_specific_permission(
        self,
    ):

        see_private_requests_permission = Permission.objects.get(
            codename="see_private_requests"
        )
        self.user.user_permissions.add(see_private_requests_permission)
        works_types = factories.WorksTypeFactory.create_batch(2)
        works_objects = factories.WorksObjectFactory.create_batch(2)

        administrative_entity = factories.PermitAdministrativeEntityFactory(
            name="privateEntity"
        )
        private_works_object_type = models.WorksObjectType.objects.create(
            works_type=works_types[0], works_object=works_objects[0], is_public=False,
        )
        private_works_object_type.administrative_entities.set([administrative_entity])
        response = self.client.get(
            reverse("permits:permit_request_select_administrative_entity",),
        )

        self.assertContains(response, "privateEntity")

    def test_work_type_step_only_show_public_requests_to_standard_user(self,):

        public_works_object_types = factories.WorksObjectTypeFactory.create_batch(
            2, is_public=True
        )
        private_works_object_type = factories.WorksObjectTypeFactory(is_public=False)
        administrative_entity = factories.PermitAdministrativeEntityFactory()
        administrative_entity.works_object_types.set(
            public_works_object_types + [private_works_object_type]
        )

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, administrative_entity=administrative_entity
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )
        self.assertEqual(
            len(get_parser(response.content).select(".form-check-label")), 2
        )

    def test_work_type_step_show_private_requests_to_user_with_specific_permission(
        self,
    ):

        see_private_requests_permission = Permission.objects.get(
            codename="see_private_requests"
        )
        self.user.user_permissions.add(see_private_requests_permission)
        public_works_object_types = factories.WorksObjectTypeFactory.create_batch(
            2, is_public=True
        )
        private_works_object_type = factories.WorksObjectTypeFactory(is_public=False)
        administrative_entity = factories.PermitAdministrativeEntityFactory()
        administrative_entity.works_object_types.set(
            public_works_object_types + [private_works_object_type]
        )

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, administrative_entity=administrative_entity
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )
        self.assertEqual(
            len(get_parser(response.content).select(".form-check-label")), 3
        )

    def test_work_type_step_show_public_requests_to_standard_user(self,):

        public_works_object_types = factories.WorksObjectTypeFactory.create_batch(
            2, is_public=True
        )
        private_works_object_type = factories.WorksObjectTypeFactory(is_public=False)
        administrative_entity = factories.PermitAdministrativeEntityFactory()
        administrative_entity.works_object_types.set(
            public_works_object_types + [private_works_object_type]
        )

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, administrative_entity=administrative_entity
        )

        permit_request.administrative_entity.works_object_types.set(
            models.WorksObjectType.objects.all()
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request,
            works_object_type=public_works_object_types[0],
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request,
            works_object_type=public_works_object_types[1],
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": permit_request.pk},
            )
            + "?types={}&types={}".format(
                public_works_object_types[0].pk, public_works_object_types[1].pk
            ),
        )
        self.assertEqual(
            len(get_parser(response.content).select(".form-check-label")), 2
        )

    def test_work_type_step_show_private_requests_to_user_with_specific_permission(
        self,
    ):

        see_private_requests_permission = Permission.objects.get(
            codename="see_private_requests"
        )
        self.user.user_permissions.add(see_private_requests_permission)

        public_works_object_types = factories.WorksObjectTypeFactory.create_batch(
            2, is_public=True
        )
        private_works_object_type = factories.WorksObjectTypeFactory(is_public=False)
        administrative_entity = factories.PermitAdministrativeEntityFactory()
        administrative_entity.works_object_types.set(
            public_works_object_types + [private_works_object_type]
        )

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, administrative_entity=administrative_entity
        )

        permit_request.administrative_entity.works_object_types.set(
            models.WorksObjectType.objects.all()
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request,
            works_object_type=public_works_object_types[0],
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request,
            works_object_type=public_works_object_types[1],
        )

        models.WorksObjectTypeChoice.objects.create(
            permit_request=permit_request, works_object_type=private_works_object_type
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_objects",
                kwargs={"permit_request_id": permit_request.pk},
            )
            + "?types={}&types={}&types={}".format(
                public_works_object_types[0].pk,
                public_works_object_types[1].pk,
                private_works_object_type.pk,
            ),
        )
        self.assertEqual(
            len(get_parser(response.content).select(".form-check-label")), 3
        )
