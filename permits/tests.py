import urllib.parse

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from bs4 import BeautifulSoup

from gpf.models import Actor, AdministrativeEntity, Department

from . import factories, models, services, views


def to_works_objects_dict(works_object_types):
    return {
        'works_objects-{}'.format(works_object_type.works_type.pk): works_object_type.pk
        for works_object_type in works_object_types
    }


def get_permit_request_works_types_ids(permit_request):
    return list(
        permit_request.works_object_types.order_by('works_type__name').values_list(
            'works_type__pk', flat=True
        ).distinct()
    )


class LoggedInUserMixin:
    def setUp(self):
        self.user = factories.UserFactory()
        self.client.login(username=self.user.username, password="password")


class LoggedInSecretariatMixin:
    def setUp(self):
        self.group = factories.SecretariatGroupFactory()
        self.administrative_entity = self.group.department.administrative_entity
        self.user = factories.SecretariatUserFactory(groups=[self.group])
        self.client.login(username=self.user.username, password="password")


class PermitRequestTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.works_types = factories.WorksTypeFactory.create_batch(2)
        self.works_objects = factories.WorksObjectFactory.create_batch(2)

        models.WorksObjectType.objects.create(
            works_type=self.works_types[0], works_object=self.works_objects[0]
        )

    def test_types_step_submit_redirects_to_objects_with_types_qs(self):
        permit_request = factories.PermitRequestFactory(author=self.user.actor)
        permit_request.administrative_entity.works_object_types.set(models.WorksObjectType.objects.all())

        response = self.client.post(
            reverse('permits:permit_request_select_types', kwargs={'permit_request_id': permit_request.pk}), data={
                'types': self.works_types[0].pk
            }
        )

        self.assertRedirects(
            response,
            reverse('permits:permit_request_select_objects', kwargs={'permit_request_id': permit_request.pk})
            + '?types={}'.format(self.works_types[0].pk)
        )

    def test_objects_step_without_qs_redirects_to_types_step(self):
        permit_request = factories.PermitRequestFactory(author=self.user.actor)
        permit_request.administrative_entity.works_object_types.set(models.WorksObjectType.objects.all())

        response = self.client.get(
            reverse('permits:permit_request_select_objects', kwargs={'permit_request_id': permit_request.pk})
        )
        self.assertRedirects(
            response, reverse('permits:permit_request_select_types', kwargs={'permit_request_id': permit_request.pk})
        )

    def test_objects_step_submit_saves_selected_object_types(self):
        permit_request = factories.PermitRequestFactory(author=self.user.actor)
        works_object_type = models.WorksObjectType.objects.first()
        permit_request.administrative_entity.works_object_types.set(models.WorksObjectType.objects.all())
        self.client.post(
            reverse('permits:permit_request_select_objects', kwargs={'permit_request_id': permit_request.pk})
            + '?types={}'.format(self.works_types[0].pk), data={
                'works_objects-{}'.format(self.works_types[0].pk): works_object_type.pk
            }
        )

        self.assertEqual(models.PermitRequest.objects.filter(works_object_types=works_object_type).count(), 1)

    def test_required_properties_can_be_left_blank(self):
        permit_request = factories.PermitRequestFactory(author=self.user.actor)
        factories.WorksObjectTypeChoiceFactory.create_batch(3, permit_request=permit_request)
        permit_request.administrative_entity.works_object_types.set(permit_request.works_object_types.all())
        prop = factories.WorksObjectPropertyFactory(is_mandatory=True)
        prop.works_object_types.set(permit_request.works_object_types.all())

        response = self.client.post(reverse('permits:permit_request_properties', kwargs={
            'permit_request_id': permit_request.pk
        }))

        self.assertRedirects(
            response, reverse('permits:permit_request_geo_time', kwargs={'permit_request_id': permit_request.pk})
        )

    def test_user_can_only_see_own_requests(self):
        permit_request = factories.PermitRequestFactory(author=factories.UserFactory().actor)

        response = self.client.get(
            reverse('permits:permit_request_select_types', kwargs={'permit_request_id': permit_request.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_user_cannot_edit_non_draft_request(self):
        permit_request = factories.PermitRequestFactory(
            author=self.user.actor, status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION
        )

        response = self.client.get(
            reverse('permits:permit_request_select_types', kwargs={'permit_request_id': permit_request.pk})
        )

        self.assertRedirects(
            response, reverse('permits:permit_request_detail', kwargs={'permit_request_id': permit_request.pk})
        )

    def test_submit_permit_request_sends_email_to_secretariat(self):
        # Create a secretariat user Yverdon (the one that will get the notification)
        group = factories.SecretariatGroupFactory()
        factories.SecretariatUserFactory(actor__email="secretariat@yverdon.ch", groups=[group])
        # This one should not receive the notification
        factories.SecretariatUserFactory(actor__email="secretariat@lausanne.ch")

        permit_request = factories.PermitRequestFactory(
            administrative_entity=group.department.administrative_entity,
            author=self.user.actor, status=models.PermitRequest.STATUS_DRAFT
        )
        self.client.post(reverse('permits:permit_request_submit', kwargs={'permit_request_id': permit_request.pk}))

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ["secretariat@yverdon.ch"])


class PermitRequestUpdateTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.permit_request = factories.PermitRequestFactory(author=self.user.actor)
        factories.WorksObjectTypeChoiceFactory.create_batch(3, permit_request=self.permit_request)
        self.permit_request.administrative_entity.works_object_types.set(self.permit_request.works_object_types.all())

    def test_types_step_submit_shows_new_objects(self):
        new_works_object_type = factories.WorksObjectTypeFactory()

        response = self.client.post(
            reverse('permits:permit_request_select_types', kwargs={'permit_request_id': self.permit_request.pk}),
            follow=True,
            data={
                'types': get_permit_request_works_types_ids(self.permit_request) + [new_works_object_type.works_type.pk]
            }
        )

        self.assertContains(response, new_works_object_type.works_type)

    def test_types_step_submit_removes_deselected_types_from_permit_request(self):
        works_object_type_id = get_permit_request_works_types_ids(self.permit_request)[0]

        self.client.post(
            reverse('permits:permit_request_select_types', kwargs={'permit_request_id': self.permit_request.pk}), data={
                'types': works_object_type_id
            }
        )

        self.permit_request.refresh_from_db()

        self.assertEqual(models.PermitRequest.objects.count(), 1)
        self.assertEqual(get_permit_request_works_types_ids(self.permit_request), [works_object_type_id])

    def test_objects_step_submit_updates_permit_request(self):
        new_works_object_type = factories.WorksObjectTypeFactory()
        self.permit_request.administrative_entity.works_object_types.add(new_works_object_type)
        current_works_object_types = list(self.permit_request.works_object_types.all())
        current_works_object_types_dict = to_works_objects_dict(current_works_object_types)
        new_works_object_types_dict = to_works_objects_dict([new_works_object_type])
        works_types_ids = get_permit_request_works_types_ids(self.permit_request) + [
            new_works_object_type.works_type.pk
        ]
        types_param = urllib.parse.urlencode({'types': works_types_ids}, doseq=True)

        self.client.post(
            (reverse('permits:permit_request_select_objects', kwargs={'permit_request_id': self.permit_request.pk})
             + '?' + types_param),
            data={**current_works_object_types_dict, **new_works_object_types_dict}
        )

        self.permit_request.refresh_from_db()

        self.assertEqual(models.PermitRequest.objects.count(), 1)
        self.assertEqual(
            set(self.permit_request.works_object_types.all()),
            set(current_works_object_types + [new_works_object_type])
        )

    def test_properties_step_submit_updates_permit_request(self):
        new_prop = factories.WorksObjectPropertyFactory()
        new_prop.works_object_types.set(self.permit_request.works_object_types.all())
        data = {
            'properties-{}_{}'.format(works_object_type.pk, new_prop.pk): 'value-{}'.format(works_object_type.pk)
            for works_object_type in self.permit_request.works_object_types.all()
        }
        self.client.post(
            reverse('permits:permit_request_properties', kwargs={'permit_request_id': self.permit_request.pk}),
            data=data
        )

        self.assertEqual(
            set(
                item['val']
                for item in services.get_properties_values(self.permit_request).values_list('value', flat=True)
            ),
            set(data.values())
        )


class PermitRequestPrefillTestCase(LoggedInUserMixin, TestCase):
    def setUp(self):
        super().setUp()
        self.permit_request = factories.PermitRequestFactory(author=self.user.actor)
        factories.WorksObjectTypeChoiceFactory.create_batch(3, permit_request=self.permit_request)
        self.permit_request.administrative_entity.works_object_types.set(self.permit_request.works_object_types.all())

    def test_types_step_preselects_types_for_existing_permit_request(self):
        response = self.client.get(
            reverse('permits:permit_request_select_types', kwargs={'permit_request_id': self.permit_request.pk})
        )
        content = response.content.decode()


        for i, works_type_id in enumerate(get_permit_request_works_types_ids(self.permit_request)):
            expected = ('<input checked="" class="form-check-input" id="id_types_{i}" name="types" title=""'
                        '  type="checkbox" value="{value}"/>').format(
                            value=works_type_id, i=i
                        )
            self.assertInHTML(expected, content)

    def test_objects_step_preselects_objects_for_existing_permit_request(self):
        response = self.client.get(
            reverse('permits:permit_request_select_objects', kwargs={'permit_request_id': self.permit_request.pk})
        )
        content = response.content.decode()

        for works_object_type in self.permit_request.works_object_types.all():
            expected = ('<input checked="" class="form-check-input" id="id_works_objects-{id}_0"'
                        ' name="works_objects-{id}" title="" type="checkbox" value="{value}"/>').format(
                            id=works_object_type.works_type.pk, value=works_object_type.pk
                        )
            self.assertInHTML(expected, content)

    def test_properties_step_prefills_properties_for_existing_permit_request(self):
        works_object_type_choice = services.get_works_object_type_choices(self.permit_request).first()
        prop = factories.WorksObjectPropertyFactory()
        prop.works_object_types.add(works_object_type_choice.works_object_type)
        prop_value = factories.WorksObjectPropertyValueFactory(
            works_object_type_choice=works_object_type_choice,
            property=prop
        )
        response = self.client.get(
            reverse('permits:permit_request_properties', kwargs={'permit_request_id': self.permit_request.pk})
        )
        content = response.content.decode()
        expected = (
            '<input type="text" name="properties-{obj_type_id}_{prop_id}" value="{value}" class="form-control"'
            ' title="" id="id_properties-{obj_type_id}_{prop_id}">'.format(
                obj_type_id=works_object_type_choice.works_object_type.pk,
                prop_id=prop.pk,
                prop_name=prop.name,
                value=prop_value.value['val']
            )
        )

        self.assertInHTML(expected, content)


class PermitRequestAmendmentTestCase(LoggedInSecretariatMixin, TestCase):
    def test_non_secretariat_user_cannot_amend_request(self):
        user = factories.UserFactory()
        self.client.login(username=user.username, password="password")

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
            author=user.actor
        )
        response = self.client.post(
            reverse('permits:permit_request_detail', kwargs={'permit_request_id': permit_request.pk}),
            data={
                'price': 300,
                'status': models.PermitRequest.STATUS_PROCESSING,
                'action': views.PermitRequestDetailView.ACTION_AMEND
            }
        )

        permit_request.refresh_from_db()

        self.assertIsNone(permit_request.price)

    def test_secretariat_can_amend_request(self):
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        self.client.post(
            reverse('permits:permit_request_detail', kwargs={'permit_request_id': permit_request.pk}),
            data={
                'price': 300,
                'status': models.PermitRequest.STATUS_PROCESSING,
                'action': views.PermitRequestDetailView.ACTION_AMEND
            }
        )

        permit_request.refresh_from_db()

        self.assertEqual(permit_request.price, 300)

    def test_secretariat_can_see_submitted_requests(self):
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.get(reverse('permits:permit_requests_list'))

        self.assertEqual(list(response.context['permitrequest_list']), [permit_request])

    def test_ask_for_supplements_shows_specific_message(self):
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse('permits:permit_request_detail', kwargs={'permit_request_id': permit_request.pk}),
            data={'status': models.PermitRequest.STATUS_AWAITING_SUPPLEMENT, 'action': views.PermitRequestDetailView.ACTION_AMEND},
            follow=True
        )

        self.assertContains(response, "Vous devez maintenant contacter le requérant par email")

    def test_secretariat_cannot_amend_permit_request_with_validation_requested(self):
        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse("permits:permit_request_detail", kwargs={"permit_request_id": permit_request.pk}),
            data={
                "price": 200,
                "action": views.PermitRequestDetailView.ACTION_AMEND
            },
        )

        self.assertEqual(response.status_code, 403)


class PermitRequestValidationRequestTestcase(LoggedInSecretariatMixin, TestCase):
    def test_secretariat_can_request_validation(self):
        validator_groups = factories.ValidatorGroupFactory.create_batch(
            2, department__administrative_entity=self.administrative_entity
        )
        validator_departments = [group.department.pk for group in validator_groups]

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse("permits:permit_request_detail", kwargs={"permit_request_id": permit_request.pk}),
            data={
                "departments": validator_departments,
                "action": views.PermitRequestDetailView.ACTION_REQUEST_VALIDATION
            },
        )

        permit_request.refresh_from_db()

        self.assertEqual(permit_request.status, models.PermitRequest.STATUS_AWAITING_VALIDATION)
        self.assertEqual(list(permit_request.validations.values_list('department', flat=True)), validator_departments)

    def test_secretariat_cannot_request_validation_for_already_validated_permit_request(self):
        validator_group = factories.ValidatorGroupFactory(department__administrative_entity=self.administrative_entity)

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_AWAITING_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.post(
            reverse("permits:permit_request_detail", kwargs={"permit_request_id": permit_request.pk}),
            data={
                "departments": [validator_group.department.pk],
                "action": views.PermitRequestDetailView.ACTION_REQUEST_VALIDATION
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_default_departments_are_checked(self):
        default_validator_groups = factories.ValidatorGroupFactory.create_batch(
            2, department__administrative_entity=self.administrative_entity, department__is_default_validator=True
        )
        non_default_validator_group = factories.ValidatorGroupFactory(
            department__administrative_entity=self.administrative_entity
        )

        permit_request = factories.PermitRequestFactory(
            status=models.PermitRequest.STATUS_SUBMITTED_FOR_VALIDATION,
            administrative_entity=self.administrative_entity,
        )
        response = self.client.get(
            reverse("permits:permit_request_detail", kwargs={"permit_request_id": permit_request.pk}),
        )

        parser = BeautifulSoup(response.content, features="html5lib")
        inputs = {
            int(input_["value"]): input_.get("checked") is not None
            for input_ in parser.select('input[name="departments"]')
        }

        self.assertDictEqual(
            inputs,
            {
                **{group.pk: True for group in default_validator_groups},
                **{non_default_validator_group.pk: False}
            }
        )
