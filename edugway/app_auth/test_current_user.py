import json
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

class CurrentUserTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # set up data for the whole test case 
        pass

    def setUp(self):
        # setup data for each test case
        pass

    def test_register_user(self):
        url = reverse('delivery:user-register')
        data = {
        	'username': 'user0001',
            'first_name': 'Registered',
            'last_name': 'Tester',
            'email': 'test.user@edugway.org',
            'new_password': 'new_Password_1',
            'confirm_password': 'new_Password_1'
        }
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
        	get_user_model().objects.get(username='user0001').has_usable_password(), True)

        # test create user with duplicate username/email
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # get a JWT fot the new user
        url = reverse('delivery-auth:user-api-token')
        data = {
            'username': 'user0001',
            'password': 'new_Password_1',
        }
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # get the users profile
        user = get_user_model().objects.get(username='user0001')
        self.client.force_authenticate(user=user)
        url = reverse('delivery:user-profile')
        response = self.client.get(url)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

