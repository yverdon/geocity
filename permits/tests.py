import urllib.parse

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core import mail
from django.test import TestCase
from django.urls import reverse

from gpf.models import Actor, AdministrativeEntity, Department

from . import factories, models, services


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


def create_user(username='admin'):
    user = get_user_model().objects.create_user(username=username, password=username)
    Actor.objects.create(user=user, firstname=username, name=username)

    return user


class LoggedInUserMixin:
    def setUp(self):
        self.user = create_user()
        self.client.login(username=self.user.username, password='admin')


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
            response, reverse('permits:permit_request_appendices', kwargs={'permit_request_id': permit_request.pk})
        )

    def test_user_can_only_see_own_requests(self):
        permit_request = factories.PermitRequestFactory(author=create_user(username='sarah').actor)

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
        secretariat_user = create_user(username="secretariat-yverdon")
        secretariat_user.actor.email = "secretariat@yverdon.ch"
        secretariat_user.actor.save()

        yverdon = AdministrativeEntity.objects.create(name="Yverdon", ofs_id=0)
        group = Group.objects.create(name="Secrétariat Yverdon")
        secretariat_user.groups.set([group])
        Department.objects.create(
            group=group, is_validator=False, is_admin=False, is_archeologist=False,
            administrative_entity=yverdon
        )

        # Create a secretariat user Lausanne (this one shouldn't get the notification)
        secretariat_user = create_user(username="secretariat-lausanne")
        secretariat_user.actor.email = "secretariat@lausanne.ch"
        secretariat_user.actor.save()

        administrative_entity = AdministrativeEntity.objects.create(name="Lausanne", ofs_id=0)
        group = Group.objects.create(name="Secrétariat Lausanne")
        secretariat_user.groups.set([group])
        Department.objects.create(
            group=group, is_validator=False, is_admin=False, is_archeologist=False,
            administrative_entity=administrative_entity
        )

        permit_request = factories.PermitRequestFactory(
            administrative_entity=yverdon,
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
