import urllib.parse

from django.urls import reverse
from django.test import TestCase, tag

from . import factories, models, services


def to_works_objects_dict(works_objects_types):
    return {
        'works_objects-{}'.format(works_object_type.works_type.pk): works_object_type.pk
        for works_object_type in works_objects_types
    }


def get_permit_request_works_types_ids(permit_request):
    return list(
        permit_request.works_objects_types.order_by('works_type__name').values_list(
            'works_type__pk', flat=True
        ).distinct()
    )


class PermitRequestTestCase(TestCase):
    def setUp(self):
        self.works_types = factories.WorksTypeFactory.create_batch(2)
        self.works_objects = factories.WorksObjectFactory.create_batch(2)

        models.WorksObjectType.objects.create(
            works_type=self.works_types[0], works_object=self.works_objects[0]
        )

    def test_types_step_submit_redirects_to_objects_with_types_qs(self):
        response = self.client.post(reverse('permits:permit_request_select_types'), data={
            'types': self.works_types[0].pk
        })

        self.assertRedirects(
            response,
            reverse('permits:permit_request_select_objects') + '?types={}'.format(self.works_types[0].pk)
        )

    def test_objects_step_without_qs_redirects_to_types_step(self):
        response = self.client.get(reverse('permits:permit_request_select_objects'))
        self.assertRedirects(response, reverse('permits:permit_request_select_types'))

    def test_objects_step_submit_saves_permit_request(self):
        works_object_type = models.WorksObjectType.objects.first()
        self.client.post(
            reverse('permits:permit_request_select_objects') + '?types={}'.format(self.works_types[0].pk), data={
                'works_objects-{}'.format(self.works_types[0].pk): works_object_type.pk
            }
        )

        self.assertEqual(models.PermitRequest.objects.filter(works_objects_types=works_object_type).count(), 1)

    @tag('wip')
    def test_required_properties_can_be_left_blank(self):
        permit_request = factories.PermitRequestFactory()
        factories.WorksObjectTypeChoiceFactory.create_batch(3, permit_request=permit_request)
        prop = factories.WorksObjectPropertyFactory(is_mandatory=True)
        prop.works_objects_types.set([
            works_object_type_choice.works_object_type
            for works_object_type_choice in services.get_works_object_type_choices(permit_request)
        ])

        response = self.client.post(reverse('permits:permit_request_properties', kwargs={
            'permit_request_id': permit_request.pk
        }))

        self.assertRedirects(
            response, reverse('permits:permit_request_appendices', kwargs={'permit_request_id': permit_request.pk})
        )


class PermitRequestUpdateTestCase(TestCase):
    def setUp(self):
        self.permit_request = factories.PermitRequestFactory()
        factories.WorksObjectTypeChoiceFactory.create_batch(3, permit_request=self.permit_request)

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
        current_works_objects_types = list(self.permit_request.works_objects_types.all())
        current_works_objects_types_dict = to_works_objects_dict(current_works_objects_types)
        new_works_objects_types_dict = to_works_objects_dict([new_works_object_type])
        works_types_ids = get_permit_request_works_types_ids(self.permit_request) + [
            new_works_object_type.works_type.pk
        ]
        types_param = urllib.parse.urlencode({'types': works_types_ids}, doseq=True)

        self.client.post(
            (reverse('permits:permit_request_select_objects', kwargs={'permit_request_id': self.permit_request.pk})
             + '?' + types_param),
            data={**current_works_objects_types_dict, **new_works_objects_types_dict}
        )

        self.permit_request.refresh_from_db()

        self.assertEqual(models.PermitRequest.objects.count(), 1)
        self.assertEqual(
            set(self.permit_request.works_objects_types.all()),
            set(current_works_objects_types + [new_works_object_type])
        )

    def test_properties_step_submit_updates_permit_request(self):
        new_prop = factories.WorksObjectPropertyFactory()
        new_prop.works_objects_types.set(self.permit_request.works_objects_types.all())
        data = {
            'properties-{}_{}'.format(works_object_type.pk, new_prop.pk): 'value-{}'.format(works_object_type.pk)
            for works_object_type in self.permit_request.works_objects_types.order_by('pk')
        }
        self.client.post(
            reverse('permits:permit_request_properties', kwargs={'permit_request_id': self.permit_request.pk}),
            data=data
        )

        self.assertEqual(
            list(services.get_properties_values(self.permit_request).order_by('pk').values_list('value', flat=True)),
            [{'val': value} for value in data.values()]
        )


class PermitRequestPrefillTestCase(TestCase):
    def setUp(self):
        self.permit_request = factories.PermitRequestFactory()
        factories.WorksObjectTypeChoiceFactory.create_batch(3, permit_request=self.permit_request)

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

        for works_object_type in self.permit_request.works_objects_types.all():
            expected = ('<input checked="" class="form-check-input" id="id_works_objects-{id}_0"'
                        ' name="works_objects-{id}" title="" type="checkbox" value="{value}"/>').format(
                            id=works_object_type.works_type.pk, value=works_object_type.pk
                        )
            self.assertInHTML(expected, content)

    def test_properties_step_prefills_properties_for_existing_permit_request(self):
        works_object_type_choice = services.get_works_object_type_choices(self.permit_request).first()
        prop = factories.WorksObjectPropertyFactory()
        prop.works_objects_types.add(works_object_type_choice.works_object_type)
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
            ' placeholder="{prop_name}" title="" id="id_properties-{obj_type_id}_{prop_id}">'.format(
                obj_type_id=works_object_type_choice.works_object_type.pk,
                prop_id=prop.pk,
                prop_name=prop.name,
                value=prop_value.value['val']
            )
        )

        self.assertInHTML(expected, content)
