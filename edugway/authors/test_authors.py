import json
from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from edugway.authors.models import Author

class AuthorTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # set up data for the whole test case 
        pass

    def setUp(self):
        # setup data for each test case
        url = reverse('author-list')
        self.author_data = {
            'title': 'Zubin John Eapen, MD',
            'headline': 'Assistant Professor of Medicine\nMember in the Duke Clinical Research Institute',
            'headline_thumbnail_url': 
            'https://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam',
            }
        response = self.client.post(url, self.author_data)
        self.author_id = response.data['id']

    def test_create_author(self):
        url = reverse('author-list')
        data = {
            'title': 'Zubin John Eapen, MD',
            'headline': 'Assistant Professor of Medicine\nMember in the Duke Clinical Research Institute',
            'headline_thumbnail_url': 
            'https://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam'
            }
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_author_invalid_url(self):
        url = reverse('author-list')
        data = {
            'title': 'Zubin John Eapen, MD',
            'headline': 'Assistant Professor of Medicine\nMember in the Duke Clinical Research Institute',
            'headline_thumbnail_url': 
            'invalid-prefix://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam'
            }
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_author_disclosure(self):
        url = reverse('author-list')
        data = {
            'title': 'Zubin John Eapen, MD',
            'headline': 'Assistant Professor of Medicine\nMember in the Duke Clinical Research Institute',
            'headline_thumbnail_url': 
            'https://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam',
            'disclosure_statement': 'I am associated with Big Pill, Inc.',
            'disclosure_expire_on': timezone.now() 
            }
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_author_disclosure(self):
        url = reverse('author-list')
        data = {
            'title': 'Zubin John Eapen, MD',
            'headline': 'Assistant Professor of Medicine\nMember in the Duke Clinical Research Institute',
            'headline_thumbnail_url': 
            'https://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam',
            'disclosure_statement': 'I am associated with Big Pill, Inc.'
            }
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_remove_author_disclosure(self):
        url = reverse('author-detail', args=[self.author_id])
        data = {
            'disclosure_statement': 'I am associated with Big Pill, Inc.',
            'disclosure_expire_on': timezone.now() 
            }
        response = self.client.patch(url, data)
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            'disclosure_statement': ' '
            }
        response = self.client.patch(url, data)
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['disclosure_expire_on'], None)
        # make sure expiration date cannot be set when no disclosure exists
        data = {
            'disclosure_expire_on': timezone.now() 
            }
        response = self.client.patch(url, data)
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['disclosure_expire_on'], None)
        # make sure expiration date cannot be set when no disclosure exists
        data = {
            'disclosure_statement': ' ',
            'disclosure_expire_on': timezone.now() 
            }
        response = self.client.patch(url, data)
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['disclosure_expire_on'], None)
        
    def test_list_authors(self):
        url = reverse('author-list')
        response = self.client.get(url)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_author(self):
        url = reverse('author-detail', args=[self.author_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_author(self):
        url = reverse('author-detail', args=[self.author_id])
        data =  {
            'title': 'Zubin John Eapen, MD - updated',
            'headline': 'Assistant Professor of Medicine\nMember in the Duke Clinical Research Institute',
            'headline_thumbnail_url': 
            'https://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam'
            }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Zubin John Eapen, MD - updated')

    def test_delete_author(self):
        url = reverse('author-detail', args=[self.author_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)