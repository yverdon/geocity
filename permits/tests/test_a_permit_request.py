# TODO split this file into multiple files
import datetime
import re
import urllib.parse
import uuid
import PIL
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

    def test_types_step_submit_redirects_to_detail_if_logged_as_backoffice(self):

        secretary_group = factories.GroupFactory(name="Secrétariat")
        department = factories.PermitDepartmentFactory(
            group=secretary_group, is_backoffice=True
        )

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_APPROVED,
            administrative_entity=department.administrative_entity,
        )
        secretary_group.user_set.add(self.user)

        response = self.client.get(
            reverse(
                "permits:permit_request_prolongation",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

        self.client.login(username=self.user.username, password="password")
        response = self.client.post(
            reverse(
                "permits:permit_request_submit",
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

    def test_types_step_submit_redirects_to_detail_if_logged_as_integrator_admin(self):

        integrator_group = factories.GroupFactory(name="Integrator")
        department = factories.PermitDepartmentFactory(
            group=integrator_group, is_integrator_admin=True
        )

        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_APPROVED,
            administrative_entity=department.administrative_entity,
        )
        integrator_group.user_set.add(self.user)

        response = self.client.get(
            reverse(
                "permits:permit_request_prolongation",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

        self.client.login(username=self.user.username, password="password")
        response = self.client.post(
            reverse(
                "permits:permit_request_submit",
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
        PIL.Image.MAX_IMAGE_PIXELS = 933120000
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

    def test_secretary_email_is_sent_when_user_treated_requested_complements(self):
        secretary_group = factories.GroupFactory(name="Secrétariat")
        department = factories.PermitDepartmentFactory(
            group=secretary_group, is_backoffice=True
        )
        factories.SecretariatUserFactory(
            groups=[secretary_group], email="secretary@geocity.ch"
        )
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_AWAITING_SUPPLEMENT,
            author=self.user.permitauthor,
            administrative_entity=department.administrative_entity,
        )
        works_type = factories.WorksTypeFactory(name="Foo type")
        works_object = factories.WorksObjectFactory()
        wot = factories.WorksObjectTypeWithoutGeometryFactory(
            works_type=works_type, works_object=works_object, needs_date=False,
        )
        permit_request.works_object_types.set([wot])
        self.client.post(
            reverse(
                "permits:permit_request_submit",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        permit_request.refresh_from_db()
        self.assertEqual(
            permit_request.status, models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["secretary@geocity.ch"])
        self.assertEqual(
            mail.outbox[0].subject,
            "La demande de compléments a été traitée (Foo type)",
        )
        self.assertIn(
            "La demande de compléments a été traitée",
            mail.outbox[0].message().as_string(),
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
        works_type = factories.WorksTypeFactory(name="Foo type")
        works_object = factories.WorksObjectFactory()
        wot = factories.WorksObjectTypeFactory(
            works_type=works_type, works_object=works_object,
        )
        permit_request.works_object_types.set([wot])

        self.client.post(
            reverse(
                "permits:permit_request_submit",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        emails = get_emails("Nouvelle demande (Foo type)")

        self.assertEqual(len(emails), 1)
        self.assertEqual(emails[0].to, ["secretariat@yverdon.ch"])

    def test_submit_permit_request_sends_email_to_services_to_notify_from_workobjectproperty(
        self,
    ):
        permit_request = factories.PermitRequestGeoTimeFactory(
            permit_request=factories.PermitRequestFactory(
                author=self.user.permitauthor, status=models.PermitRequest.STATUS_DRAFT,
            )
        ).permit_request

        work_object_type_choice = factories.WorksObjectTypeChoiceFactory(
            permit_request=permit_request
        )

        prop = factories.WorksObjectPropertyFactory(
            services_to_notify="test-send-1@geocity.ch, test-send-2@geocity.ch, test-i-am-not-an-email,  ,\n\n\n",
            input_type=models.WorksObjectProperty.INPUT_TYPE_CHECKBOX,
        )

        prop.works_object_types.set(permit_request.works_object_types.all())
        factories.WorksObjectPropertyValueFactory(
            property=prop,
            works_object_type_choice=work_object_type_choice,
            value={"val": True},
        )
        self.client.post(
            reverse(
                "permits:permit_request_submit_confirmed",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )

        self.assertEqual(len(mail.outbox), 3)
        self.assertIn(
            mail.outbox[0].to, [["test-send-1@geocity.ch"], ["test-send-2@geocity.ch"]]
        )

        self.assertEqual(
            mail.outbox[0].subject, "Votre service à été mentionné dans une demande"
        )
        self.assertIn(
            "Une nouvelle demande mentionnant votre service vient d'être soumise.",
            mail.outbox[0].message().as_string(),
        )

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

        today = date.today()
        starts_at = today + datetime.timedelta(days=(int(settings.MIN_START_DELAY) + 2))
        ends_at = today + datetime.timedelta(days=(int(settings.MIN_START_DELAY) + 1))
        self.geotime_step_formset_data.update(
            {
                "form-0-starts_at": [starts_at.strftime("%Y-%m-%d 14:00:00+02:00")],
                "form-0-ends_at": [ends_at.strftime("%Y-%m-%d 14:00:00+02:00")],
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

    def test_start_date_is_limited_by_work_object_types_with_biggest_start_delay(self):
        group = factories.SecretariatGroupFactory()
        work_object_type_1 = factories.WorksObjectTypeFactory(start_delay=3,)
        work_object_type_2 = factories.WorksObjectTypeFactory(start_delay=1,)

        permit_request = factories.PermitRequestGeoTimeFactory(
            permit_request=factories.PermitRequestFactory(
                administrative_entity=group.permitdepartment.administrative_entity,
                author=self.user.permitauthor,
                status=models.PermitRequest.STATUS_DRAFT,
            )
        ).permit_request

        permit_request.works_object_types.set([work_object_type_1, work_object_type_2])

        resulted_start_at = permit_request.get_min_starts_at().date()
        expected_start_at = date.today() + datetime.timedelta(days=3)

        self.assertEqual(resulted_start_at, expected_start_at)

    def test_start_date_limit_falls_back_to_setting(self):
        today = date.today()
        group = factories.SecretariatGroupFactory()
        work_object_type = factories.WorksObjectTypeFactory()

        permit_request = factories.PermitRequestGeoTimeFactory(
            permit_request=factories.PermitRequestFactory(
                administrative_entity=group.permitdepartment.administrative_entity,
                author=self.user.permitauthor,
                status=models.PermitRequest.STATUS_DRAFT,
            )
        ).permit_request

        permit_request.works_object_types.set([work_object_type])

        self.assertEqual(
            permit_request.get_min_starts_at().date(),
            today + datetime.timedelta(days=int(settings.MIN_START_DELAY)),
        )

    def test_start_date_cant_be_of_limit(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        works_object_type = factories.WorksObjectTypeWithoutGeometryFactory(
            needs_date=True, start_delay=3,
        )
        permit_request.works_object_types.set([works_object_type])
        today = date.today()
        start_at = today + datetime.timedelta(days=1)  # Must be >= 3 to be valid
        self.geotime_step_formset_data.update(
            {
                "form-0-starts_at": [start_at.strftime("%Y-%m-%d 14:00:00+02:00")],
                "form-0-ends_at": [start_at.strftime("%Y-%m-%d 16:00:00+02:00")],
            }
        )
        response = self.client.post(
            reverse(
                "permits:permit_request_geo_time",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=self.geotime_step_formset_data,
        )
        self.assertIn("starts_at", response.context["formset"].errors[0])

    def test_start_date_limit_is_set_to_0(self):
        group = factories.SecretariatGroupFactory()
        work_object_type = factories.WorksObjectTypeFactory(start_delay=0)
        permit_request = factories.PermitRequestGeoTimeFactory(
            permit_request=factories.PermitRequestFactory(
                administrative_entity=group.permitdepartment.administrative_entity,
                author=self.user.permitauthor,
                status=models.PermitRequest.STATUS_DRAFT,
            )
        ).permit_request
        permit_request.works_object_types.set([work_object_type])

        self.assertEqual(permit_request.get_min_starts_at().date(), date.today())

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
            {"entityfilter": "first"},
            follow=True,
        )

        new_permit_request = models.PermitRequest.objects.last()

        parser = get_parser(response.content)
        content = response.content.decode()
        self.assertInHTML("Sélectionnez le ou les type(s)", content)
        self.assertRedirects(
            response,
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": new_permit_request.id},
            ),
        )

        response2 = self.client.get(
            reverse(
                "permits:permit_request_select_administrative_entity",
                kwargs={"permit_request_id": new_permit_request.id},
            ),
            {"entityfilter": "first"},
            follow=True,
        )
        parser2 = get_parser(response2.content)
        content2 = response2.content.decode()
        element_parsed = parser2.select(".form-check-label")

        # Check that selected item is there
        self.assertEqual(1, len(element_parsed))
        # Check that filtered items are NOT there
        self.assertNotContains(response, administrative_entities[1].name)
        self.assertNotContains(response, administrative_entities[2].name)
        self.assertInHTML(administrative_entities[0].name, content2)

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
            {"entityfilter": "wrongtag"},
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
            {"entityfilter": ["first", "second"]},
        )

        parser = get_parser(response.content)
        element_parsed = parser.select(".form-check-label")

        content = response.content.decode()

        self.assertEqual(2, len(element_parsed))
        self.assertInHTML(administrative_entities[0].name, content)
        self.assertInHTML(administrative_entities[1].name, content)

    def test_work_type_is_filtered_by_tag(self):
        additional_works_type = factories.WorksTypeFactory()
        additional_works_objects = factories.WorksObjectFactory()

        models.WorksObjectType.objects.create(
            works_type=additional_works_type,
            works_object=additional_works_objects,
            is_public=True,
        )

        self.works_types[0].tags.add("work_type_a")
        self.works_types[1].tags.add("work_type_a")
        additional_works_type.tags.add("work_type_b")
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        permit_request.administrative_entity.works_object_types.set(
            models.WorksObjectType.objects.all()
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            )
            + "?typefilter=work_type_a"
        )

        parser = get_parser(response.content)
        element_parsed = parser.select(".form-check-label")

        # Check that 2 types are visibles
        self.assertEqual(2, len(element_parsed))

    def test_work_type_is_not_filtered_by_bad_tag(self):
        additional_works_type = factories.WorksTypeFactory()
        additional_works_objects = factories.WorksObjectFactory()

        models.WorksObjectType.objects.create(
            works_type=additional_works_type,
            works_object=additional_works_objects,
            is_public=True,
        )

        self.works_types[0].tags.add("work_type_a")
        self.works_types[1].tags.add("work_type_a")
        additional_works_type.tags.add("work_type_b")
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        permit_request.administrative_entity.works_object_types.set(
            models.WorksObjectType.objects.all()
        )

        response = self.client.get(
            reverse(
                "permits:permit_request_select_types",
                kwargs={"permit_request_id": permit_request.pk},
            )
            + "?typefilter=badtag"
        )

        parser = get_parser(response.content)
        element_parsed = parser.select(".form-check-label")

        # Check that 3 types are visibles
        self.assertEqual(3, len(element_parsed))

    def test_missing_mandatory_list_values_show_error(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory(permit_request=permit_request)
        works_object_type = permit_request.works_object_types.first()
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        list_single_prop = factories.WorksObjectPropertyFactory(
            input_type=models.WorksObjectProperty.INPUT_TYPE_LIST_SINGLE,
            choices="foo\nbar",
            is_mandatory=True,
        )
        list_multiple_prop = factories.WorksObjectPropertyFactory(
            input_type=models.WorksObjectProperty.INPUT_TYPE_LIST_MULTIPLE,
            choices="foo\nbar",
            is_mandatory=True,
        )
        for prop in [list_single_prop, list_multiple_prop]:
            prop.works_object_types.set(permit_request.works_object_types.all())

        data = {
            f"properties-{works_object_type.pk}_{list_single_prop.pk}": "",
        }

        response = self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=data,
        )
        self.assertFormError(
            response,
            "permit_request_form",
            f"{works_object_type.pk}_{list_single_prop.pk}",
            ["Ce champ est obligatoire."],
        )
        self.assertFormError(
            response,
            "permit_request_form",
            f"{works_object_type.pk}_{list_multiple_prop.pk}",
            ["Ce champ est obligatoire."],
        )

    def test_list_multiple_value_is_stored_as_list(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory(permit_request=permit_request)
        works_object_type = permit_request.works_object_types.first()
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        list_multiple_prop = factories.WorksObjectPropertyFactory(
            input_type=models.WorksObjectProperty.INPUT_TYPE_LIST_MULTIPLE,
            choices="foo\nbar",
        )
        list_multiple_prop.works_object_types.set(
            permit_request.works_object_types.all()
        )

        data = {
            f"properties-{works_object_type.pk}_{list_multiple_prop.pk}": [
                "foo",
                "bar",
            ],
        }

        response = self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=data,
        )
        self.assertEqual(
            services.get_property_value(
                models.WorksObjectPropertyValue.objects.first()
            ),
            ["foo", "bar"],
        )

    def test_list_single_value_is_stored_as_list(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory(permit_request=permit_request)
        works_object_type = permit_request.works_object_types.first()
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        list_multiple_prop = factories.WorksObjectPropertyFactory(
            input_type=models.WorksObjectProperty.INPUT_TYPE_LIST_MULTIPLE,
            choices="foo\nbar",
        )
        list_multiple_prop.works_object_types.set(
            permit_request.works_object_types.all()
        )

        data = {f"properties-{works_object_type.pk}_{list_multiple_prop.pk}": "foo"}

        response = self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=data,
        )
        self.assertEqual(
            services.get_property_value(
                models.WorksObjectPropertyValue.objects.first()
            ),
            ["foo"],
        )

    def test_input_is_restricted_to_list_values(self):
        permit_request = factories.PermitRequestFactory(author=self.user.permitauthor)
        factories.WorksObjectTypeChoiceFactory(permit_request=permit_request)
        works_object_type = permit_request.works_object_types.first()
        permit_request.administrative_entity.works_object_types.set(
            permit_request.works_object_types.all()
        )
        list_single_prop = factories.WorksObjectPropertyFactory(
            input_type=models.WorksObjectProperty.INPUT_TYPE_LIST_SINGLE,
            choices="foo\nbar",
            is_mandatory=True,
        )
        list_multiple_prop = factories.WorksObjectPropertyFactory(
            input_type=models.WorksObjectProperty.INPUT_TYPE_LIST_MULTIPLE,
            choices="foo\nbar",
            is_mandatory=True,
        )
        for prop in [list_single_prop, list_multiple_prop]:
            prop.works_object_types.set(permit_request.works_object_types.all())

        data = {
            f"properties-{works_object_type.pk}_{list_single_prop.pk}": "baz",
            f"properties-{works_object_type.pk}_{list_multiple_prop.pk}": ["baz"],
        }

        response = self.client.post(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data=data,
        )

        self.assertFormError(
            response,
            "permit_request_form",
            f"{works_object_type.pk}_{list_single_prop.pk}",
            ["Sélectionnez un choix valide. baz n’en fait pas partie."],
        )
        self.assertFormError(
            response,
            "permit_request_form",
            f"{works_object_type.pk}_{list_multiple_prop.pk}",
            ["Sélectionnez un choix valide. baz n’en fait pas partie."],
        )


class PermitRequestProlongationTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.wot_normal = factories.WorksObjectTypeFactory()
        self.wot_normal_no_date = factories.WorksObjectTypeFactory(needs_date=False)
        self.wot_prolongable_no_date = factories.WorksObjectTypeFactory(
            needs_date=False, permit_duration=30,
        )
        self.wot_prolongable_with_date = factories.WorksObjectTypeFactory(
            needs_date=True, permit_duration=60,
        )
        self.wot_prolongable_no_date_with_reminder = factories.WorksObjectTypeFactory(
            needs_date=False,
            permit_duration=90,
            expiration_reminder=True,
            days_before_reminder=5,
        )
        self.wot_prolongable_with_date_and_reminder = factories.WorksObjectTypeFactory(
            needs_date=True,
            permit_duration=120,
            expiration_reminder=True,
            days_before_reminder=10,
        )

        secretary_group = factories.GroupFactory(name="Secrétariat")
        self.department = factories.PermitDepartmentFactory(
            group=secretary_group, is_backoffice=True
        )
        self.secretariat = factories.SecretariatUserFactory(
            groups=[secretary_group], email="secretary@geocity.ch"
        )

    def test_user_cannot_request_permit_prolongation_if_permit_is_not_prolongable(
        self,
    ):
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_APPROVED,
        )
        permit_request.works_object_types.set([self.wot_normal])
        factories.PermitRequestGeoTimeFactory(permit_request=permit_request)

        # Permit list
        response = self.client.get(reverse("permits:permit_requests_list",))
        parser = get_parser(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Demander une prolongation")

        # Prolongation form
        response = self.client.get(
            reverse(
                "permits:permit_request_prolongation",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
        )
        parser = get_parser(response.content)
        alert = parser.find(
            "div", string="La demande de permis ne peut pas être prolongée."
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(alert))
        self.assertNotContains(response, "Demander une prolongation")

    def test_user_cannot_request_permit_prolongation_if_it_prolongation_is_processing(
        self,
    ):
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_PROCESSING,
            prolongation_status=models.PermitRequest.PROLONGATION_STATUS_PENDING,
            prolongation_date=timezone.now() + datetime.timedelta(days=90),
        )
        permit_request.works_object_types.set([self.wot_prolongable_with_date])
        factories.PermitRequestGeoTimeFactory(permit_request=permit_request)

        # Prolongation form
        response = self.client.get(
            reverse(
                "permits:permit_request_prolongation",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
        )
        parser = get_parser(response.content)
        regex = re.compile(
            r"^Une demande de prolongation pour le permis #[0-9]* est en attente ou a été refusée."
        )
        alert = parser.find("div", string=regex)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(alert))
        self.assertNotContains(response, "Demander une prolongation")

    def test_user_cannot_request_permit_prolongation_if_it_has_been_rejected(self,):
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_AWAITING_SUPPLEMENT,
            prolongation_status=models.PermitRequest.PROLONGATION_STATUS_REJECTED,
            prolongation_date=timezone.now() + datetime.timedelta(days=90),
        )
        permit_request.works_object_types.set([self.wot_prolongable_with_date])
        factories.PermitRequestGeoTimeFactory(permit_request=permit_request)

        # Prolongation form
        response = self.client.get(
            reverse(
                "permits:permit_request_prolongation",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
        )
        parser = get_parser(response.content)
        regex = re.compile(
            r"^Une demande de prolongation pour le permis #[0-9]* est en attente ou a été refusée."
        )
        alert = parser.find("div", string=regex)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(alert))
        self.assertNotContains(response, "Demander une prolongation")

    def test_secretariat_cannot_request_permit_prolongation_via_form_if_it_is_not_the_permit_author(
        self,
    ):
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor,
            status=models.PermitRequest.STATUS_AWAITING_SUPPLEMENT,
        )
        permit_request.works_object_types.set(
            [self.wot_prolongable_no_date_with_reminder]
        )
        factories.PermitRequestGeoTimeFactory(permit_request=permit_request)

        permit_request.administrative_entity.departments.set([self.department])

        self.client.login(username=self.secretariat, password="password")

        # Prolongation form
        response = self.client.get(
            reverse(
                "permits:permit_request_prolongation",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
        )

        parser = get_parser(response.content)
        regex = re.compile(
            r"^Vous ne pouvez pas demander une prolongation pour le permis"
        )
        alert = parser.find("div", string=regex)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(alert))
        self.assertNotContains(response, "Demander une prolongation")

    def test_user_can_request_permit_prolongation(self,):
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_APPROVED
        )
        permit_request.works_object_types.set(
            [self.wot_prolongable_with_date_and_reminder]
        )
        factories.PermitRequestGeoTimeFactory(permit_request=permit_request)
        permit_request.administrative_entity.departments.set([self.department])

        # Prolongation form
        response = self.client.get(
            reverse(
                "permits:permit_request_prolongation",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )
        parser = get_parser(response.content)

        title = parser.find("h3", string="Demande de prolongation de permis")
        widget = parser.find(
            "input",
            title="Cliquer sur le champ et sélectionner la nouvelle date de fin planifiée",
        )
        self.assertEqual(1, len(title))
        self.assertEqual("id_prolongation_date", widget.get("id"))

        # Post
        prolongation_date = timezone.now() + datetime.timedelta(days=90)
        response = self.client.post(
            reverse(
                "permits:permit_request_prolongation",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
            data={"prolongation_date": prolongation_date},
        )
        parser = get_parser(response.content)
        regex = re.compile(r"^Prolongation en attente")
        icon_prolongation_processing = parser.findAll("i", title=regex)
        icon_permit_expired = parser.findAll("i", title="Demande échue")
        expected_subject_regex = re.compile(
            r"Une demande de prolongation vient d'être soumise"
        )

        permit_request.refresh_from_db()

        self.assertRedirects(response, reverse("permits:permit_requests_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(icon_prolongation_processing))
        self.assertEqual(1, len(icon_permit_expired))
        self.assertEqual(
            models.PermitRequest.PROLONGATION_STATUS_PENDING,
            permit_request.prolongation_status,
        )
        self.assertEqual(prolongation_date, permit_request.prolongation_date)
        # Emails
        self.assertIn("secretary@geocity.ch", mail.outbox[0].to)
        self.assertRegex(mail.outbox[0].subject, expected_subject_regex)
        self.assertRegex(mail.outbox[0].message().as_string(), expected_subject_regex)

    def test_permit_prolongation_request_must_be_after_original_end_date(self,):
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_APPROVED
        )
        permit_request.works_object_types.set(
            [self.wot_prolongable_with_date_and_reminder]
        )
        factories.PermitRequestGeoTimeFactory(
            permit_request=permit_request,
            starts_at=timezone.now() - datetime.timedelta(days=30),
            ends_at=timezone.now(),
        )

        # Post

        response = self.client.post(
            reverse(
                "permits:permit_request_prolongation",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
            data={"prolongation_date": timezone.now() - datetime.timedelta(days=1)},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "La date de prolongation doit être postérieure à la date originale de fin",
        )

    # TESTS FOR THE SECRETARIAT
    def test_secretariat_can_prolonge_or_permit_request_without_user_asking(self,):
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_APPROVED,
        )
        permit_request.works_object_types.set([self.wot_prolongable_with_date])
        factories.PermitRequestGeoTimeFactory(permit_request=permit_request)
        permit_request.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        # Prolongation form on permit details
        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
        )

        parser = get_parser(response.content)

        prolong_form_div = parser.find("div", id="prolong")
        prolong_form = prolong_form_div.find("form")
        no_requested_prolongation_msg = prolong_form.find("small")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(no_requested_prolongation_msg))

        # Post the form
        prolongation_date = timezone.now() + datetime.timedelta(days=90)

        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
            data={
                "prolongation_date": prolongation_date,
                "prolongation_status": models.PermitRequest.PROLONGATION_STATUS_APPROVED,
                "prolongation_comment": "Prolonged! I got the power!",
                "action": models.ACTION_PROLONG,
            },
        )
        permit_request.refresh_from_db()

        parser = get_parser(response.content)

        regex = re.compile(r"^Prolongation en attente")
        icon_prolongation_processing = parser.findAll("i", title=regex)
        icon_prolongation_approved = parser.findAll("i", title="Demande renouvelée")
        expected_subject_regex = re.compile(
            r"^Votre demande #[0-9]* a bien été prolongée."
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("permits:permit_requests_list"))
        self.assertEqual(0, len(icon_prolongation_processing))
        self.assertEqual(1, len(icon_prolongation_approved))
        self.assertEqual(
            models.PermitRequest.PROLONGATION_STATUS_APPROVED,
            permit_request.prolongation_status,
        )
        self.assertEqual(prolongation_date, permit_request.prolongation_date)
        self.assertEqual(
            "Prolonged! I got the power!", permit_request.prolongation_comment
        )

        self.assertIn("user@test.com", mail.outbox[0].to)
        self.assertRegex(mail.outbox[0].subject, expected_subject_regex)
        self.assertIn(
            "Nous vous informons que votre demande de prolongation a été traitée.",
            mail.outbox[0].message().as_string(),
        )

    def test_secretariat_can_reject_permit_request(self,):
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_APPROVED,
        )
        permit_request.works_object_types.set([self.wot_prolongable_with_date])
        factories.PermitRequestGeoTimeFactory(permit_request=permit_request)
        permit_request.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        # Post the form
        prolongation_date = timezone.now() + datetime.timedelta(days=90)

        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            follow=True,
            data={
                "prolongation_date": prolongation_date,
                "prolongation_status": models.PermitRequest.PROLONGATION_STATUS_REJECTED,
                "prolongation_comment": "Rejected! Because I say so!",
                "action": models.ACTION_PROLONG,
            },
        )
        permit_request.refresh_from_db()

        parser = get_parser(response.content)

        regex = re.compile(r"^Prolongation en attente")
        icon_prolongation_processing = parser.findAll("i", title=regex)
        icon_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")
        expected_subject_regex = re.compile(
            r"^La prolongation de votre demande #[0-9]* a été refusée."
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse("permits:permit_requests_list"))
        self.assertEqual(0, len(icon_prolongation_processing))
        self.assertEqual(1, len(icon_prolongation_rejected))
        self.assertEqual(
            models.PermitRequest.PROLONGATION_STATUS_REJECTED,
            permit_request.prolongation_status,
        )
        self.assertEqual(prolongation_date, permit_request.prolongation_date)
        self.assertEqual(
            "Rejected! Because I say so!", permit_request.prolongation_comment
        )

        self.assertRegex(mail.outbox[0].subject, expected_subject_regex)
        self.assertIn(
            "Nous vous informons que votre demande de prolongation a été traitée.",
            mail.outbox[0].message().as_string(),
        )

    def test_secretariat_prolonge_form_is_disabled_on_bad_permit_request_status(self,):
        permit_request = factories.PermitRequestFactory(
            author=self.user.permitauthor, status=models.PermitRequest.STATUS_RECEIVED,
        )
        permit_request.works_object_types.set([self.wot_prolongable_with_date])
        factories.PermitRequestGeoTimeFactory(permit_request=permit_request)
        permit_request.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        # Prolongation form on permit details
        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
        )

        parser = get_parser(response.content)
        prolong_form_div = parser.find("div", id="prolong")
        prolong_form = prolong_form_div.find("form")
        self.assertTrue("disabled" in str(prolong_form))
        self.assertEqual(response.status_code, 200)

    def test_user_cannot_see_prolongation_icons_nor_info_if_expired_permit_is_draft(
        self,
    ):
        # Draft - No action icons - No expired/renew icons

        permit_request_draft = factories.PermitRequestFactory(
            validated_at=timezone.now(),
            status=models.PermitRequest.STATUS_DRAFT,
            author=self.user.permitauthor,
        )
        permit_request_draft.works_object_types.set([self.wot_normal])
        ends_at_draft = timezone.now()
        factories.PermitRequestGeoTimeFactory(
            permit_request=permit_request_draft,
            starts_at=timezone.now() - datetime.timedelta(days=30),
            ends_at=ends_at_draft,
        )
        response = self.client.get(reverse("permits:permit_requests_list",))
        parser = get_parser(response.content)

        info_expired_permits = parser.findAll("i", title="Demande échue")
        info_prolonged_permits = parser.findAll("i", title="Demande renouvelée")
        action_request_prolongation = parser.findAll(
            "a", title="Demander une prolongation"
        )
        action_prolongation_requested = parser.findAll(
            "i", title=re.compile(r"Prolongation en attente")
        )
        action_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(info_expired_permits))
        self.assertEqual(0, len(info_prolonged_permits))
        self.assertEqual(0, len(action_request_prolongation))
        self.assertEqual(0, len(action_prolongation_requested))
        self.assertEqual(0, len(action_prolongation_rejected))

    def test_user_can_see_prolongation_icons_if_permit_is_about_to_expire(self,):
        # Expired within delay of reminder  - Action icon - No expired/renew icons
        permit_request_expired = factories.PermitRequestFactory(
            validated_at=timezone.now(),
            status=models.PermitRequest.STATUS_APPROVED,
            author=self.user.permitauthor,
        )
        permit_request_expired.works_object_types.set(
            [self.wot_prolongable_with_date_and_reminder]
        )
        ends_at_expired = timezone.now() + datetime.timedelta(days=5)
        factories.PermitRequestGeoTimeFactory(
            permit_request=permit_request_expired,
            starts_at=timezone.now() - datetime.timedelta(days=120),
            ends_at=ends_at_expired,
        )

        response = self.client.get(reverse("permits:permit_requests_list",))
        parser = get_parser(response.content)

        info_expired_permits = parser.findAll("i", title="Demande échue")
        info_prolonged_permits = parser.findAll("i", title="Demande renouvelée")
        action_request_prolongation = parser.findAll(
            "a", title="Demander une prolongation"
        )
        action_prolongation_requested = parser.findAll(
            "i", title=re.compile(r"Prolongation en attente")
        )
        action_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(info_expired_permits))
        self.assertEqual(0, len(info_prolonged_permits))
        self.assertEqual(1, len(action_request_prolongation))
        self.assertEqual(0, len(action_prolongation_requested))
        self.assertEqual(0, len(action_prolongation_rejected))

    def test_user_can_see_prolongation_info_icons_if_permit_is_prolonged(self,):
        # Prolonged  - No action icons - Renew icons - Date fin = prolongation_date
        prolongation_date_prolonged = timezone.now() + datetime.timedelta(days=365)
        permit_request_prolonged = factories.PermitRequestFactory(
            validated_at=timezone.now(),
            status=models.PermitRequest.STATUS_APPROVED,
            author=self.user.permitauthor,
            prolongation_date=prolongation_date_prolonged,
            prolongation_status=models.PermitRequest.PROLONGATION_STATUS_APPROVED,
        )
        permit_request_prolonged.works_object_types.set(
            [self.wot_prolongable_with_date_and_reminder]
        )
        ends_at_prolonged = timezone.now() + datetime.timedelta(days=5)
        factories.PermitRequestGeoTimeFactory(
            permit_request=permit_request_prolonged,
            starts_at=timezone.now() - datetime.timedelta(days=120),
            ends_at=ends_at_prolonged,
        )

        response = self.client.get(reverse("permits:permit_requests_list",))
        parser = get_parser(response.content)

        info_expired_permits = parser.findAll("i", title="Demande échue")
        info_prolonged_permits = parser.findAll("i", title="Demande renouvelée")
        action_request_prolongation = parser.findAll(
            "a", title="Demander une prolongation"
        )
        action_prolongation_requested = parser.findAll(
            "i", title=re.compile(r"Prolongation en attente")
        )
        action_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(info_expired_permits))
        self.assertEqual(1, len(info_prolonged_permits))
        self.assertEqual(0, len(action_request_prolongation))
        self.assertEqual(0, len(action_prolongation_requested))
        self.assertEqual(0, len(action_prolongation_rejected))

    def test_user_can_see_prolongation_info_icons_if_permit_prolongation_is_requested(
        self,
    ):

        # Prolongation Requested
        prolongation_date_requested = timezone.now() + datetime.timedelta(days=365)
        permit_request_prolongation_requested = factories.PermitRequestFactory(
            validated_at=timezone.now(),
            status=models.PermitRequest.STATUS_APPROVED,
            author=self.user.permitauthor,
            prolongation_date=prolongation_date_requested,
            prolongation_status=models.PermitRequest.PROLONGATION_STATUS_PENDING,
        )
        permit_request_prolongation_requested.works_object_types.set(
            [self.wot_prolongable_no_date_with_reminder]
        )
        ends_at_requested = timezone.now() + datetime.timedelta(days=4)
        factories.PermitRequestGeoTimeFactory(
            permit_request=permit_request_prolongation_requested,
            starts_at=timezone.now() - datetime.timedelta(days=120),
            ends_at=ends_at_requested,
        )

        response = self.client.get(reverse("permits:permit_requests_list",))
        parser = get_parser(response.content)

        info_expired_permits = parser.findAll("i", title="Demande échue")
        info_prolonged_permits = parser.findAll("i", title="Demande renouvelée")
        action_request_prolongation = parser.findAll(
            "a", title="Demander une prolongation"
        )
        action_prolongation_requested = parser.findAll(
            "i", title=re.compile(r"Prolongation en attente")
        )
        action_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, len(info_expired_permits))
        self.assertEqual(0, len(info_prolonged_permits))
        self.assertEqual(0, len(action_request_prolongation))
        self.assertEqual(1, len(action_prolongation_requested))
        self.assertEqual(0, len(action_prolongation_rejected))

    def test_user_can_see_prolongation_info_icons_if_permit_prolongation_is_rejected(
        self,
    ):

        # Prolongation Rejected
        prolongation_date_rejected = timezone.now() + datetime.timedelta(days=300)
        permit_request_prolongation_rejected = factories.PermitRequestFactory(
            validated_at=timezone.now(),
            status=models.PermitRequest.STATUS_APPROVED,
            author=self.user.permitauthor,
            prolongation_date=prolongation_date_rejected,
            prolongation_status=models.PermitRequest.PROLONGATION_STATUS_REJECTED,
        )
        permit_request_prolongation_rejected.works_object_types.set(
            [self.wot_prolongable_no_date_with_reminder]
        )
        ends_at_rejected = timezone.now() - datetime.timedelta(days=3)
        factories.PermitRequestGeoTimeFactory(
            permit_request=permit_request_prolongation_rejected,
            starts_at=timezone.now() - datetime.timedelta(days=120),
            ends_at=ends_at_rejected,
        )

        response = self.client.get(reverse("permits:permit_requests_list",))
        parser = get_parser(response.content)

        info_expired_permits = parser.findAll("i", title="Demande échue")
        info_prolonged_permits = parser.findAll("i", title="Demande renouvelée")
        action_request_prolongation = parser.findAll(
            "a", title="Demander une prolongation"
        )
        action_prolongation_requested = parser.findAll(
            "i", title=re.compile(r"Prolongation en attente")
        )
        action_prolongation_rejected = parser.findAll("i", title="Prolongation refusée")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(info_expired_permits))
        self.assertEqual(0, len(info_prolonged_permits))
        self.assertEqual(0, len(action_request_prolongation))
        self.assertEqual(0, len(action_prolongation_requested))
        self.assertEqual(1, len(action_prolongation_rejected))

    def test_secretariat_can_see_prolongation_buttons_if_wot_has_prolongation_enabled(
        self,
    ):

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_APPROVED,
        )
        permit_request.works_object_types.set([self.wot_prolongable_with_date])
        permit_request.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".tab-pane#prolong button")), 2,
        )

    def test_secretariat_can_see_prolongation_buttons_if_at_least_one_wot_has_prolongation_enabled(
        self,
    ):

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_APPROVED,
        )
        permit_request.works_object_types.set(
            [self.wot_prolongable_with_date, self.wot_normal]
        )
        permit_request.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".tab-pane#prolong button")), 2,
        )

    def test_secretariat_cannot_see_prolongation_buttons_if_wot_has_not_prolongation_enabled(
        self,
    ):

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_APPROVED,
        )
        permit_request.works_object_types.set([self.wot_normal])
        permit_request.administrative_entity.departments.set([self.department])
        self.client.login(username=self.secretariat, password="password")

        response = self.client.get(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            )
        )
        parser = get_parser(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(parser.select(".tab-pane#prolong button")), 0,
        )


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

        expected = '<textarea name="properties-{obj_type_id}_{prop_id}" cols="40" rows="1" placeholder="ex: {placeholder}" class="textarea form-control" title="{help_text}" id="id_properties-{obj_type_id}_{prop_id}">{value}'.format(
            obj_type_id=works_object_type_choice.works_object_type.pk,
            prop_id=prop.pk,
            prop_name=prop.name,
            value=prop_value.value["val"],
            placeholder=prop.placeholder,
            help_text=prop.help_text,
        )

        expected_help_text = '<small id="hint_id_properties-{obj_type_id}_{prop_id}" class="form-text text-muted">{help_text}</small>'.format(
            help_text=prop.help_text,
            obj_type_id=works_object_type_choice.works_object_type.pk,
            prop_id=prop.pk,
        )

        self.assertInHTML(expected, content)
        self.assertInHTML(expected_help_text, content)

    def test_properties_step_shows_title_and_additional_text(self):
        works_object_type_choice = services.get_works_object_type_choices(
            self.permit_request
        ).first()

        prop_title = factories.WorksObjectPropertyFactoryTypeTitle()
        prop_title.works_object_types.add(works_object_type_choice.works_object_type)

        response = self.client.get(
            reverse(
                "permits:permit_request_properties",
                kwargs={"permit_request_id": self.permit_request.pk},
            )
        )
        content = response.content.decode()
        expected = "<h5 class='propertyTitle'>{prop_name}</h5>".format(
            prop_name=prop_title.name,
        )

        expected_help_text = "<small>{help_text}</small>".format(
            help_text=prop_title.help_text
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
        factories.PermitRequestGeoTimeFactory(permit_request=permit_request)
        response = self.client.get(reverse("permits:permit_requests_list"))

        self.assertEqual(list(response.context["permitrequest_list"]), [permit_request])

    def test_ask_for_supplements_shows_specific_message(self):
        work_object_type_1 = factories.WorksObjectTypeFactory()
        work_object_type_2 = factories.WorksObjectTypeFactory()
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        permit_request.works_object_types.set([work_object_type_1, work_object_type_2])
        factories.PermitRequestGeoTimeFactory(permit_request=permit_request)
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

    def test_secretariat_can_see_print_buttons(self):
        first_works_object_type = factories.WorksObjectTypeFactory()
        second_works_object_type = factories.WorksObjectTypeFactory()

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

    def test_secretariat_cannot_see_print_buttons_if_not_configured(self,):
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

    def test_secretariat_can_see_directives(self):
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
            len(parser.select(".tab-pane#directives span.directive_description")), 2,
        )

    def test_secretariat_cannot_see_directives_if_not_configured(self,):
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
            len(parser.select(".tab-pane#directives span.directive_description")), 0,
        )

    def test_email_to_author_is_sent_when_secretariat_acknowledges_reception(self):
        user = factories.UserFactory(email="user@geocity.com")
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=user.permitauthor,
        )
        works_type = factories.WorksTypeFactory(name="Foo type")
        works_object = factories.WorksObjectFactory()
        wot = factories.WorksObjectTypeFactory(
            works_type=works_type, works_object=works_object,
        )
        permit_request.works_object_types.set([wot])
        factories.PermitRequestGeoTimeFactory(permit_request=permit_request)
        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": permit_request.pk},
            ),
            data={
                "status": models.PermitRequest.STATUS_RECEIVED,
                "action": models.ACTION_AMEND,
            },
            follow=True,
        )

        permit_request.refresh_from_db()
        self.assertEqual(permit_request.status, models.PermitRequest.STATUS_RECEIVED)
        self.assertContains(response, "compléments")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])
        self.assertEqual(
            mail.outbox[0].subject,
            "Votre annonce a été prise en compte et classée (Foo type)",
        )
        self.assertIn(
            "Nous vous informons que votre annonce a été prise en compte et classée.",
            mail.outbox[0].message().as_string(),
        )


class AdministrativeEntitySecretaryEmailTestcase(TestCase):
    def setUp(self):
        self.user = factories.UserFactory(email="user@geocity.com")
        self.administrative_entity_expeditor = factories.PermitAdministrativeEntityFactory(
            expeditor_email="geocity_rocks@geocity.ch", expeditor_name="Geocity Rocks"
        )
        self.group = factories.SecretariatGroupFactory(
            department__administrative_entity=self.administrative_entity_expeditor
        )
        self.secretary = factories.SecretariatUserFactory(groups=[self.group])
        self.client.login(username=self.secretary.username, password="password")

        self.permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity_expeditor,
            author=self.user.permitauthor,
        )

    def test_secretary_email_and_name_are_set_for_the_administrative_entity(self):
        works_type = factories.WorksTypeFactory(name="Foo type")
        works_object = factories.WorksObjectFactory()
        wot = factories.WorksObjectTypeFactory(
            works_type=works_type, works_object=works_object,
        )
        self.permit_request.works_object_types.set([wot])

        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data={
                "status": models.PermitRequest.STATUS_RECEIVED,
                "action": models.ACTION_AMEND,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].from_email, "Geocity Rocks <geocity_rocks@geocity.ch>"
        )
        self.assertEqual(
            mail.outbox[0].subject,
            "Votre annonce a été prise en compte et classée (Foo type)",
        )
        self.assertIn(
            "Nous vous informons que votre annonce a été prise en compte et classée.",
            mail.outbox[0].message().as_string(),
        )

    def test_just_secretary_email_is_set_for_the_administrative_entity(self):
        works_type = factories.WorksTypeFactory(name="Foo type")
        works_object = factories.WorksObjectFactory()
        wot = factories.WorksObjectTypeFactory(
            works_type=works_type, works_object=works_object,
        )
        self.permit_request.works_object_types.set([wot])
        self.administrative_entity_expeditor = (
            models.PermitAdministrativeEntity.objects.first()
        )
        self.administrative_entity_expeditor.expeditor_email = (
            "geocity_rocks@geocity.ch"
        )
        self.administrative_entity_expeditor.expeditor_name = ""
        self.administrative_entity_expeditor.save()
        self.administrative_entity_expeditor.refresh_from_db()

        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data={
                "status": models.PermitRequest.STATUS_RECEIVED,
                "action": models.ACTION_AMEND,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, "<geocity_rocks@geocity.ch>")
        self.assertEqual(
            mail.outbox[0].subject,
            "Votre annonce a été prise en compte et classée (Foo type)",
        )
        self.assertIn(
            "Nous vous informons que votre annonce a été prise en compte et classée.",
            mail.outbox[0].message().as_string(),
        )

    def test_no_secretary_email_is_set_for_the_administrative_entity(self):
        works_type = factories.WorksTypeFactory(name="Foo type")
        works_object = factories.WorksObjectFactory()
        wot = factories.WorksObjectTypeFactory(
            works_type=works_type, works_object=works_object,
        )
        self.permit_request.works_object_types.set([wot])
        self.administrative_entity_expeditor = (
            models.PermitAdministrativeEntity.objects.first()
        )
        self.administrative_entity_expeditor.expeditor_email = ""
        self.administrative_entity_expeditor.expeditor_name = "Geocity Rocks"
        self.administrative_entity_expeditor.save()
        self.administrative_entity_expeditor.refresh_from_db()

        response = self.client.post(
            reverse(
                "permits:permit_request_detail",
                kwargs={"permit_request_id": self.permit_request.pk},
            ),
            data={
                "status": models.PermitRequest.STATUS_RECEIVED,
                "action": models.ACTION_AMEND,
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)

        self.assertNotEqual(mail.outbox[0].from_email, "geocity_rocks@geocity.ch")
        self.assertEqual(mail.outbox[0].from_email, "your_noreply_email")
        self.assertEqual(
            mail.outbox[0].subject,
            "Votre annonce a été prise en compte et classée (Foo type)",
        )
        self.assertIn(
            "Nous vous informons que votre annonce a été prise en compte et classée.",
            mail.outbox[0].message().as_string(),
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
        validator_user = factories.ValidatorUserFactory(
            groups=[validator_groups[0]], email="validator@geocity.ch"
        )
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
        factories.PermitRequestGeoTimeFactory(permit_request=validation.permit_request)

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
            groups=[validation.department.group, factories.ValidatorGroupFactory()],
            email="validator@geocity.ch",
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

    def test_secretary_email_is_sent_when_permit_request_is_validated(self):
        validation = factories.PermitRequestValidationFactory()
        secretary_group = factories.GroupFactory(name="Secrétariat")
        department = factories.PermitDepartmentFactory(
            group=secretary_group, is_backoffice=True
        )
        factories.SecretariatUserFactory(
            groups=[secretary_group], email="secretary@geocity.ch"
        )
        validation.permit_request.administrative_entity.departments.set([department])
        works_type = factories.WorksTypeFactory(name="Foo type")
        works_object = factories.WorksObjectFactory()
        wot = factories.WorksObjectTypeFactory(
            works_type=works_type, works_object=works_object,
        )
        validation.permit_request.works_object_types.set([wot])

        validator = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()],
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
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["secretary@geocity.ch"])
        self.assertEqual(
            mail.outbox[0].subject,
            "Les services chargés de la validation d'une demande ont donné leur préavis (Foo type)",
        )
        self.assertIn(
            "Les services chargés de la validation d'une demande ont donné leur préavis",
            mail.outbox[0].message().as_string(),
        )


class PermitRequestClassifyTestCase(TestCase):
    def setUp(self):
        self.secretariat_group = factories.SecretariatGroupFactory()
        self.administrative_entity = (
            self.secretariat_group.permitdepartment.administrative_entity
        )
        self.administrative_entity.custom_signature = "a custom signature for email"
        self.administrative_entity.save()
        self.secretariat_user = factories.SecretariatUserFactory(
            groups=[self.secretariat_group]
        )

        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity
        )
        self.validator_user = factories.ValidatorUserFactory(
            groups=[validation.department.group, factories.ValidatorGroupFactory()]
        )

    def test_secretariat_can_approve_permit_request_and_email_to_author_is_sent(self):

        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity,
            permit_request__status=models.PermitRequest.STATUS_PROCESSING,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
            permit_request__author__user__email="user@geocity.com",
        )
        works_type = factories.WorksTypeFactory(name="Foo type")
        works_object = factories.WorksObjectFactory()
        wot = factories.WorksObjectTypeFactory(
            works_type=works_type, works_object=works_object,
        )
        validation.permit_request.works_object_types.set([wot])

        self.client.login(username=self.secretariat_user.username, password="password")
        factories.PermitRequestGeoTimeFactory(permit_request=validation.permit_request)
        response = self.client.post(
            reverse(
                "permits:permit_request_approve",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={
                "validation_pdf": SimpleUploadedFile("file.pdf", "contents".encode())
            },
        )

        self.assertRedirects(
            response,
            reverse("permits:permit_requests_list"),
            fetch_redirect_response=False,
        )
        validation.permit_request.refresh_from_db()
        self.assertEqual(
            validation.permit_request.status, models.PermitRequest.STATUS_APPROVED
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])
        self.assertEqual(
            mail.outbox[0].subject, "Votre demande a été traitée et classée (Foo type)",
        )
        self.assertIn(
            "Nous vous informons que votre demande a été traitée et classée.",
            mail.outbox[0].message().as_string(),
        )
        self.assertIn(
            "a custom signature for email", mail.outbox[0].message().as_string(),
        )

    def test_secretariat_can_reject_permit_request_and_email_to_author_is_sent(self):

        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity,
            permit_request__status=models.PermitRequest.STATUS_PROCESSING,
            validation_status=models.PermitRequestValidation.STATUS_REJECTED,
            permit_request__author__user__email="user@geocity.com",
        )
        works_type = factories.WorksTypeFactory(name="Foo type")
        works_object = factories.WorksObjectFactory()
        wot = factories.WorksObjectTypeFactory(
            works_type=works_type, works_object=works_object,
        )
        validation.permit_request.works_object_types.set([wot])

        self.client.login(username=self.secretariat_user.username, password="password")
        factories.PermitRequestGeoTimeFactory(permit_request=validation.permit_request)
        response = self.client.post(
            reverse(
                "permits:permit_request_reject",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
            data={
                "validation_pdf": SimpleUploadedFile("file.pdf", "contents".encode()),
            },
        )

        self.assertRedirects(
            response,
            reverse("permits:permit_requests_list"),
            fetch_redirect_response=False,
        )
        validation.permit_request.refresh_from_db()
        self.assertEqual(
            validation.permit_request.status, models.PermitRequest.STATUS_REJECTED
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])
        self.assertEqual(
            mail.outbox[0].subject, "Votre demande a été traitée et classée (Foo type)",
        )
        self.assertIn(
            "Nous vous informons que votre demande a été traitée et classée.",
            mail.outbox[0].message().as_string(),
        )
        self.assertIn(
            "a custom signature for email", mail.outbox[0].message().as_string(),
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
            permit_request__status=models.PermitRequest.STATUS_PROCESSING,
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

    def test_email_to_services_is_sent_when_secretariat_classifies_permit_request(self):
        works_type_1 = factories.WorksTypeFactory(name="Foo type")
        works_type_2 = factories.WorksTypeFactory(name="Bar type")
        works_object = factories.WorksObjectFactory()
        wot = factories.WorksObjectTypeFactory(
            requires_validation_document=False,
            notify_services=True,
            services_to_notify="test-send-1@geocity.ch, test-send-2@geocity.ch, test-i-am-not-an-email,  ,\n\n\n",
            works_type=works_type_1,
            works_object=works_object,
        )
        wot2 = factories.WorksObjectTypeFactory(
            requires_validation_document=False,
            notify_services=True,
            services_to_notify="not-repeated-email@liip.ch, test-send-1@geocity.ch, \n, test-send-2@geocity.ch, test-i-am-not-an-email,  ,",
            works_type=works_type_2,
            works_object=works_object,
        )
        validation = factories.PermitRequestValidationFactory(
            permit_request__administrative_entity=self.administrative_entity,
            permit_request__status=models.PermitRequest.STATUS_PROCESSING,
            validation_status=models.PermitRequestValidation.STATUS_APPROVED,
            permit_request__author__user__email="user@geocity.com",
        )
        validation.permit_request.works_object_types.set([wot, wot2])
        factories.PermitRequestGeoTimeFactory(permit_request=validation.permit_request)

        self.client.login(username=self.secretariat_user.username, password="password")
        response = self.client.post(
            reverse(
                "permits:permit_request_approve",
                kwargs={"permit_request_id": validation.permit_request.pk},
            ),
        )

        self.assertRedirects(
            response,
            reverse("permits:permit_requests_list"),
            fetch_redirect_response=False,
        )
        validation.permit_request.refresh_from_db()
        self.assertEqual(
            validation.permit_request.status, models.PermitRequest.STATUS_APPROVED
        )
        # Only valid emails are sent, not repeated emails.
        self.assertEqual(len(mail.outbox), 4)
        self.assertEqual(mail.outbox[0].to, ["user@geocity.com"])

        self.assertIn(
            "Votre demande a été traitée et classée", mail.outbox[0].subject,
        )

        self.assertIn(
            "Bar type", mail.outbox[0].subject,
        )

        self.assertIn(
            "Foo type", mail.outbox[0].subject,
        )

        self.assertIn(
            "Nous vous informons que votre demande a été traitée et classée.",
            mail.outbox[0].message().as_string(),
        )

        services_message_content = "Nous vous informons qu'une demande a été traitée et classée par le secrétariat."
        valid_services_emails = [
            "not-repeated-email@liip.ch",
            "test-send-2@geocity.ch",
            "test-send-1@geocity.ch",
        ]
        self.assertIn(
            "a custom signature for email", mail.outbox[0].message().as_string(),
        )
        self.assertTrue(mail.outbox[1].to[0] in valid_services_emails)
        self.assertIn(services_message_content, mail.outbox[1].message().as_string())
        self.assertTrue(mail.outbox[2].to[0] in valid_services_emails)
        self.assertIn(services_message_content, mail.outbox[2].message().as_string())
        self.assertTrue(mail.outbox[3].to[0] in valid_services_emails)
        self.assertIn(services_message_content, mail.outbox[3].message().as_string())


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
            permit_request__status=models.PermitRequest.STATUS_PROCESSING,
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
            models.PermitRequest.STATUS_PROCESSING,
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

        # Fixme without any WorksObject created, returns 404

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
