import json

from django.test import TestCase, Client


class TestSetupClass(TestCase):
    fixtures = ['initial.json']

    def setUp(self):
        super().setUp()
        self.client = Client()

    def test_order_status_change(self):
        # order 7 has status 3.

        # downgrade status.
        response = self.client.patch('/api/v1/order/7/', data=json.dumps({'status': 2}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # cancel order - won't be changed because its already travelling to deliver.
        response = self.client.patch('/api/v1/order/7/', data=json.dumps({'status': 5}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # change status to delivered.
        response = self.client.patch('/api/v1/order/7/', data=json.dumps({'status': 4}), content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # status will not change, because its delivered
        response = self.client.patch('/api/v1/order/7/', data=json.dumps({'status': 3}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # cancel order - success
        response = self.client.patch('/api/v1/order/23/', data=json.dumps({'status': 5}), content_type='application/json')
        self.assertEqual(response.status_code, 200)
