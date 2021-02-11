from django.test import TestCase
from rest_framework.test import APIClient

from kn_homework.shipments_api.models import Shipment


class ShipmentViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.shipment1 = Shipment(sender='Marco Polo', receiver='Donata Badoer', description='Delicious Chinese Tea', tracking_code='CHN-1')
        self.shipment2 = Shipment(sender='Marco Polo', receiver='Nicole Anna Defuseh', description='Herbs from China', tracking_code='CHN-2')
        self.shipment1.save()
        self.shipment2.save()

    def test_list(self):
        expected = {self.shipment1, self.shipment2}

        response = self.client.get('/shipments/', content_type='application/json')
        actual = {Shipment(**item) for item in response.data}

        assert actual == expected

    def test_retrieve(self):
        expected = self.shipment1

        response = self.client.get('/shipments/{}/'.format(self.shipment1.id), content_type='application/json')
        actual = Shipment(**response.data)

        assert actual == expected

    def test_retrieve_when_not_found(self):
        expected = 404

        response = self.client.get('/shipments/999/', content_type='application/json')
        actual = response.status_code

        assert actual == expected

    def test_create(self):
        params = dict(sender='Donata Badoer',
                      receiver='Marco Polo',
                      description='A Letter from Wife',
                      tracking_code='ITA-1')
        expected = Shipment(**params)

        response = self.client.post('/shipments/', data=params, format='json')
        new_instance = Shipment(**response.data)
        actual = Shipment.objects.get(pk=new_instance.id)

        assert actual.sender == expected.sender
        assert actual.receiver == expected.receiver
        assert actual.description == expected.description
        assert actual.tracking_code == expected.tracking_code

    def test_create_when_required_fields_are_missing(self):
        expected = 422

        response = self.client.post('/shipments/', data={}, format='json')
        actual = response.status_code

        assert actual == expected

    def test_update(self):
        params = dict(sender='Marco Polo',
                      receiver='Niccolò Polo',
                      description='Herbs from China',
                      tracking_code='CHN-2')
        expected = Shipment(**params)

        self.client.put('/shipments/{}/'.format(self.shipment2.id), data=params, format='json')
        actual = Shipment.objects.get(pk=self.shipment2.id)

        assert actual.sender == expected.sender
        assert actual.receiver == expected.receiver
        assert actual.description == expected.description
        assert actual.tracking_code == expected.tracking_code

    def test_update_with_incomplete_data(self):
        expected = 422

        response = self.client.put('/shipments/{}/'.format(self.shipment2.id), data={'receiver': 'Niccolò Polo'}, format='json')
        actual = response.status_code

        assert actual == expected

    def test_destroy(self):
        self.client.delete('/shipments/{}/'.format(self.shipment1.id), format='json')

        assert not Shipment.objects.filter(pk=self.shipment1.id).count()
