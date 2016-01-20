import json
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from edugway.forms.models import Form, Field

class FormTests(APITestCase):
	@classmethod
	def setUpTestData(cls):
		# set up data for the whole test case
		pass

	def setUp(self):
		# setup data for each test case
		url = reverse('form-list')
		self.form_data = {'type': Form.TYPE_ASSESSMENT, 'title': 'sample form'}
		response = self.client.post(url, self.form_data)
		self.form_id = response.data['id']

	def test_create_form(self):
		url = reverse('form-list')
		data = {'type': Form.TYPE_ASSESSMENT, 'title': 'sample form'}
		response = self.client.post(url, data)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_list_forms(self):
		url = reverse('form-list')
		response = self.client.get(url)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_form(self):
		url = reverse('form-detail', args=[self.form_id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_form(self):
		url = reverse('form-detail', args=[self.form_id])
		data = {'type': Form.TYPE_EVALUATION, 'title': 'sample form - updated'}
		response = self.client.put(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['title'], 'sample form - updated')
		# verify type field was not modified - it is immutable
		self.assertEqual(response.data['type'], Form.TYPE_ASSESSMENT)

	def test_patch_form(self):
		url = reverse('form-detail', args=[self.form_id])
		data = {'type': Form.TYPE_EVALUATION, 'title': 'sample form - patched'}
		response = self.client.patch(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['title'], 'sample form - patched')
		# verify type field was not modified - it is immutable
		self.assertEqual(response.data['type'], Form.TYPE_ASSESSMENT)

	def test_delete_form(self):
		url = reverse('form-detail', args=[self.form_id])
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_create_field(self):
		url = reverse('form-fields', args=[self.form_id])
		data = {'type': Field.TYPE_RADIO, 'label': 'sample field'}
		response = self.client.post(url, data)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
