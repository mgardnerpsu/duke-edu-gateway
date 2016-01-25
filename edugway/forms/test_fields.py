import json
from underscore import _
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from edugway.forms.models import Form, Field

class FieldTests(APITestCase):
	@classmethod
	def setUpTestData(cls):
		# set up data for the whole test case
		pass

	def setUp(self):
		# setup data for each test case
		# create a form
		url = reverse('form-list')
		self.form_data = {'type': Form.TYPE_ASSESSMENT, 'title': 'sample form'}
		response = self.client.post(url, self.form_data)
		self.form_id = response.data['id']
		# create a field
		url = reverse('form-fields', args=[self.form_id])
		self.field_data = {'type': Field.TYPE_RADIO, 'label': 'sample field'}
		response = self.client.post(url, self.field_data)
		self.field_id = response.data['id']

	def test_list_fields(self):
		url = reverse('form-fields', args=[self.form_id])
		response = self.client.get(url)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_field(self):
		url = reverse('form-fields-detail', args=[self.field_id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_field(self):
		url = reverse('form-fields-detail', args=[self.field_id])
		data = {'type': Field.TYPE_DROPDOWN, 'label': 'sample field - updated'}
		response = self.client.put(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['label'], 'sample field - updated')

	def test_patch_field(self):
		url = reverse('form-fields-detail', args=[self.field_id])
		data = {'type': Field.TYPE_DROPDOWN, 'label': 'sample field - patched'}
		response = self.client.patch(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['label'], 'sample field - patched')

	def test_delete_field(self):
		url = reverse('form-fields-detail', args=[self.field_id])
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		
	def test_create_choice(self):
		url = reverse('form-fields-choices', args=[self.field_id])
		data = {'label': 'sample choice'}
		response = self.client.post(url, data)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class ReSequenceFieldsTests(APITestCase):
	@classmethod
	def setUpTestData(cls):
		# set up data for the whole test case
		# create form/fields to ensure there are no namespace issues when
		# re-sequencing fields for test case specific forms
		client = APIClient()
		url = reverse('form-list')
		form_data = {'type': Form.TYPE_ASSESSMENT, 'title': 'sample form'}
		response = client.post(url, form_data)
		form_id = response.data['id']
		# create fields 
		url = reverse('form-fields', args=[form_id])
		for i in range(1,11):
			data = {'type': Field.TYPE_RADIO, 'label': 'sample field'}	
			response = client.post(url, data)

	def setUp(self):
		# setup data for each test case
		# create a form
		url = reverse('form-list')
		self.form_data = {'type': Form.TYPE_ASSESSMENT, 'title': 'sample form'}
		response = self.client.post(url, self.form_data)
		self.form_id = response.data['id']
		# create fields 
		url = reverse('form-fields', args=[self.form_id])
		self.fields = {}
		for i in range(1,6):
			data = {'type': Field.TYPE_RADIO, 'label': 'sample field - ' + str(i)}	
			response = self.client.post(url, data)
			self.fields[i] = response.data

	def test_move_field_down(self):
		# move field 5 down (last field)
		url = reverse('form-fields-move-down', args=[self.fields[5]['id']])
		response = self.client.put(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# verify field 5 was not changed - it is the last field
		self.assertEqual(response.data['sequence'], 5)
		self.assertEqual(response.data['label'], 'sample field - 5')
		# move field 3 down
		url = reverse('form-fields-move-down', args=[self.fields[3]['id']])
		response = self.client.put(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# verify 3 moved to 4
		self.assertEqual(response.data['sequence'], 4)
		self.assertEqual(response.data['name'], 'field-4')
		self.assertEqual(response.data['label'], 'sample field - 3')
		# verify 4 moved to 3
		url = reverse('form-fields-detail', args=[self.fields[4]['id']])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['sequence'], 3)
		self.assertEqual(response.data['name'], 'field-3')
		self.assertEqual(response.data['label'], 'sample field - 4')
		# get all the fields for visual review
		url = reverse('form-fields', args=[self.form_id])
		response = self.client.get(url)
		response = self.client.get(url)
		self.assertEqual(_.pluck(response.data, 'sequence'), [1, 2, 3, 4, 5])
		self.assertEqual(_.pluck(response.data, 'name'), ['field-1', 'field-2', 'field-3', 'field-4', 'field-5'])
		#print(json.dumps(response.data, indent=4))

	def test_move_field_up(self):
		# move field 1 up (first field)
		url = reverse('form-fields-move-up', args=[self.fields[1]['id']])
		response = self.client.put(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# verify field 1 was not changed - it it the first field
		self.assertEqual(response.data['sequence'], 1)
		self.assertEqual(response.data['label'], 'sample field - 1')
		# move field 4 up
		url = reverse('form-fields-move-up', args=[self.fields[4]['id']])
		response = self.client.put(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# verify 4 moved to 3
		self.assertEqual(response.data['sequence'], 3)
		self.assertEqual(response.data['name'], 'field-3')
		self.assertEqual(response.data['label'], 'sample field - 4')
		# verify 3 moved to 4
		url = reverse('form-fields-detail', args=[self.fields[3]['id']])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['sequence'], 4)
		self.assertEqual(response.data['name'], 'field-4')
		self.assertEqual(response.data['label'], 'sample field - 3')
		# get all the fields for visual review
		url = reverse('form-fields', args=[self.form_id])
		response = self.client.get(url)
		self.assertEqual(_.pluck(response.data, 'sequence'), [1, 2, 3, 4, 5])
		self.assertEqual(_.pluck(response.data, 'name'), ['field-1', 'field-2', 'field-3', 'field-4', 'field-5'])
		#print(json.dumps(response.data, indent=4))

	def test_delete_field(self):
		# delete field 2
		url = reverse('form-fields-detail', args=[self.fields[2]['id']])
		response = self.client.delete(url)
		# verify fields were re-sequenced
		url = reverse('form-fields', args=[self.form_id])
		response = self.client.get(url)
		self.assertEqual(_.pluck(response.data, 'sequence'), [1, 2, 3, 4])
		self.assertEqual(_.pluck(response.data, 'name'), ['field-1', 'field-2', 'field-3', 'field-4'])
		#print(json.dumps(response.data, indent=4))
