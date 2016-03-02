import json
from underscore import _
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from edugway.forms.models import Form, Field

class ChoiceTests(APITestCase):
	@classmethod
	def setUpTestData(cls):
		# set up data for the whole test case
		pass

	def setUp(self):
		# setup data for each test case
		# create a form
		url = reverse('content:form-list')
		self.form_data = {'type': Form.TYPE_ASSESSMENT, 'title': 'sample form'}
		response = self.client.post(url, self.form_data)
		self.form_id = response.data['id']
		# create a field
		url = reverse('content:form-fields', args=[self.form_id])
		self.field_data = {'type': Field.TYPE_RADIO, 'label': 'sample field'}
		response = self.client.post(url, self.field_data)
		self.field_id = response.data['id']
		# create a choice
		url = reverse('content:form-fields-choices', args=[self.field_id])
		self.choice_data = {'label': 'sample choice'}
		response = self.client.post(url, self.choice_data)
		self.choice_id = response.data['id']
		
	def test_list_choices(self):
		url = reverse('content:form-fields-choices', args=[self.field_id])
		response = self.client.get(url)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_choice(self):
		url = reverse('content:field-choices-detail', args=[self.choice_id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_update_choice(self):
		url = reverse('content:field-choices-detail', args=[self.choice_id])
		data = {'label': 'sample choice - updated'}
		response = self.client.put(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['label'], 'sample choice - updated')

	def test_patch_choice(self):
		url = reverse('content:field-choices-detail', args=[self.choice_id])
		data = {'label': 'sample choice - patched'}
		response = self.client.patch(url, data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['label'], 'sample choice - patched')

	def test_delete_choice(self):
		url = reverse('content:field-choices-detail', args=[self.choice_id])
		response = self.client.delete(url)
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ReSequenceChoicesTests(APITestCase):
	@classmethod
	def setUpTestData(cls):
		# set up data for the whole test case
		# create form/field/choices to ensure there are no namespace issues when
		# re-sequencing choices for test case specific forms
		client = APIClient()
		url = reverse('content:form-list')
		form_data = {'type': Form.TYPE_ASSESSMENT, 'title': 'sample form'}
		response = client.post(url, form_data)
		form_id = response.data['id']
		# create field
		url = reverse('content:form-fields', args=[form_id])
		field_data = {'type': Field.TYPE_RADIO, 'label': 'sample field'}	
		response = client.post(url, field_data)
		field_id = response.data['id']
		# create choices 
		url = reverse('content:form-fields-choices', args=[field_id])
		for i in range(1,11):
			data = {'label': 'sample choice'}	
			response = client.post(url, data)

	def setUp(self):
		# setup data for each test case
		# create a form
		url = reverse('content:form-list')
		self.form_data = {'type': Form.TYPE_ASSESSMENT, 'title': 'sample form'}
		response = self.client.post(url, self.form_data)
		self.form_id = response.data['id']
		# create field 
		url = reverse('content:form-fields', args=[self.form_id])
		data = {'type': Field.TYPE_RADIO, 'label': 'sample field - ' + str(1)}	
		response = self.client.post(url, data)
		self.field_id = response.data['id']
		# create choices
		url = reverse('content:form-fields-choices', args=[self.field_id])
		self.choices = {}
		for i in range(1,6):
			data = {'label': 'sample choice - ' + str(i)}	
			response = self.client.post(url, data)
			self.choices[i] = response.data

	def test_move_choice_down(self):
		# move choice 5 down (last choice)
		url = reverse('content:field-choices-move-seq-down', args=[self.choices[5]['id']])
		response = self.client.put(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# verify choice 5 was not changed - it is the last choice
		self.assertEqual(response.data['sequence'], 5)
		self.assertEqual(response.data['label'], 'sample choice - 5')
		# move choice 3 down
		url = reverse('content:field-choices-move-seq-down', args=[self.choices[3]['id']])
		response = self.client.put(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# verify 3 moved to 4
		self.assertEqual(response.data['sequence'], 4)
		self.assertEqual(response.data['name'], 'choice-4')
		self.assertEqual(response.data['label'], 'sample choice - 3')
		# verify 4 moved to 3
		url = reverse('content:field-choices-detail', args=[self.choices[4]['id']])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['sequence'], 3)
		self.assertEqual(response.data['name'], 'choice-3')
		self.assertEqual(response.data['label'], 'sample choice - 4')
		# get all the choices for visual review
		url = reverse('content:form-fields-choices', args=[self.field_id])
		response = self.client.get(url)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(_.pluck(response.data, 'sequence'), [1, 2, 3, 4, 5])
		self.assertEqual(_.pluck(response.data, 'name'), ['choice-1', 'choice-2', 'choice-3', 'choice-4', 'choice-5'])

	def test_move_choice_up(self):
		# move choice 1 up (first choice)
		url = reverse('content:field-choices-move-seq-up', args=[self.choices[1]['id']])
		response = self.client.put(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# verify choice 1 was not changed - it is the first choice
		self.assertEqual(response.data['sequence'], 1)
		self.assertEqual(response.data['label'], 'sample choice - 1')
		# move choice 4 up
		url = reverse('content:field-choices-move-seq-up', args=[self.choices[4]['id']])
		response = self.client.put(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# verify 4 moved to 3
		self.assertEqual(response.data['sequence'], 3)
		self.assertEqual(response.data['name'], 'choice-3')
		self.assertEqual(response.data['label'], 'sample choice - 4')
		# verify 3 moved to 4
		url = reverse('content:field-choices-detail', args=[self.choices[3]['id']])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['sequence'], 4)
		self.assertEqual(response.data['name'], 'choice-4')
		self.assertEqual(response.data['label'], 'sample choice - 3')
		# get all the choices for visual review
		url = reverse('content:form-fields-choices', args=[self.field_id])
		response = self.client.get(url)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(_.pluck(response.data, 'sequence'), [1, 2, 3, 4, 5])
		self.assertEqual(_.pluck(response.data, 'name'), ['choice-1', 'choice-2', 'choice-3', 'choice-4', 'choice-5'])

	def test_delete_choice(self):
		# delete choice 2
		url = reverse('content:field-choices-detail', args=[self.choices[2]['id']])
		response = self.client.delete(url)
		# verify choices were re-sequenced
		url = reverse('content:form-fields-choices', args=[self.field_id])
		response = self.client.get(url)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(_.pluck(response.data, 'sequence'), [1, 2, 3, 4])
		self.assertEqual(_.pluck(response.data, 'name'), ['choice-1', 'choice-2', 'choice-3', 'choice-4'])

	def test_mark_correct_choice(self):
		# mark choice 2, 3, 4 correct
		url = reverse('content:field-choices-mark-correct', args=[self.choices[2]['id']])
		response = self.client.put(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		url = reverse('content:field-choices-mark-correct', args=[self.choices[3]['id']])
		response = self.client.put(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		url = reverse('content:field-choices-mark-correct', args=[self.choices[4]['id']])
		response = self.client.put(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# verify only choice 4 is correct
		url = reverse('content:form-fields-choices', args=[self.field_id])
		response = self.client.get(url)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(_.pluck(response.data, 'is_correct'), [False, False, False, True, False])

