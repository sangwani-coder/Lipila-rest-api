import os
from django.contrib.auth.models import User
from api.models import LipilaCollection, User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from uuid import UUID
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class LipilaCollectionViewTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username='test_user1')
        self.user1 = User.objects.create(username='test_user2')

    def test_create_payment_success(self):
        url = reverse('payments-list')
        
        data = {'payee':self.user.id, 'amount': '100', 'payer': '0809123456', 'reference_id': 'examplepayer'}
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(LipilaCollection.objects.count(), 1)
        self.assertEqual(LipilaCollection.objects.get().status, 'accepted')
        # Attempt to convert the response to a UUID object
        try:
            # Attempt to convert the response to a UUID object
            UUID(LipilaCollection.objects.get().reference_id)
            self.assertTrue(True)  # Test passes if conversion is successful
        except ValueError:
            self.fail("get_uuid4 did not return a valid UUID string.")

    def test_create_lipila_fail_validation(self):
        url = reverse('payments-list')
        data = {'payer': 'lipila', 'amount': 'invalid'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(LipilaCollection.objects.count(), 0)


    def test_create_nonlipila_fail_payer(self):
        url = reverse('payments-list')
        data = {'amount': 100, 'payer': '0809123456'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(LipilaCollection.objects.count(), 0)

    def test_payment_with_user_instance_success(self):
        LipilaCollection.objects.create(payee=self.user, amount=100, status='success')
        url = reverse('payments-list')
        response = self.client.get(url, {'payee': self.user.username})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_fail_no_payee(self):
        url = reverse('payments-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_fail_payee_not_found(self):
        url = reverse('payments-list')
        response = self.client.get(url, {'payee': 'not_a_user'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

