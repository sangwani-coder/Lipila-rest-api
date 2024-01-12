"""
file: test_handler.py
This file contains tests for the 3rd Party API communication
in external_api_handler.py
"""


from django.test import TestCase, Client
from api.momo.mtn import Collections
from api.helpers import get_uuid4


class HandlerTestCase(TestCase):
    """Tests for the application views."""

    @classmethod
    def setUpTestData(cls):
        print('\n\n.................................')
        print('....... Testing External API ....')
        print('---------------------------------\n\n')

    def setUp(self):
        self.momo = Collections()
        self.ref = get_uuid4()
        self.user = self.momo.create_api_user()
        self.key = self.momo.get_api_key()
        self.token = self.momo.get_api_token()
        self.payer0 = self.momo.request_to_pay('36654', '0969620939', '56797356')
       
    def test_x_reference_id(self):
        """ Test the x_reference id creation"""        
        self.assertEqual(type(self.ref), str)

    def test_api_user(self):
        """ Test Sandbox user creation"""
        self.assertEqual(self.user.status_code, 201)

    def test_api_key(self):
        """Tesk Api key creaStion"""
        self.assertEqual(self.key.status_code, 201)

    def test_api_token(self):
        """ Test API access token creation"""
        self.assertEqual(self.token.status_code, 200)

    def test_request_to_pay(self):
        """Test request to pay method"""
        self.assertEqual(self.payer0.status_code, 202)
        get_payment_status = self.momo.get_payment_status() # check the payment status
        self.assertEqual(get_payment_status.status_code, 200) # assert successful

        check_user_status = self.momo.validate_account_holder()
        self.assertEqual(check_user_status.status_code, 200) #assert successful


    def test_value_errors(self):
        """ Test the length of PartyId"""
        self.assertRaises(ValueError,
                          self.momo.request_to_pay,
                          '36654', '096962', '56797356')
        self.assertRaises(ValueError,
                          self.momo.request_to_pay,
                          '36654', '0969620978895774', '56797356')
        self.assertRaises(ValueError,
                          self.momo.request_to_pay,
                          '5', '0969620978', '56797356')

    def test_type_errors(self):
        """Test the type of paramateres"""
        self.assertRaises(TypeError,
                          self.momo.request_to_pay,
                          12345, '0969620939', '56797356')
        self.assertRaises(TypeError,
                          self.momo.request_to_pay,
                          '12345', 969620939, '56797356')
        self.assertRaises(TypeError,
                          self.momo.request_to_pay,
                          '12345', '0969620939', 56797356)
        



