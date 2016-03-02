import json
from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

class AuthorTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # set up data for the whole test case 
        pass

    def setUp(self):
        # setup data for each test case
        url = reverse('content:author-list')
        self.author_data = {
            'title': 'Zubin John Eapen, MD',
            'headline': 'Assistant Professor of Medicine\nMember in the Duke Clinical Research Institute',
            'thumbnails_headline_url': 
            'https://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam',
            'disclosure_statement': 'The author has no industry disclosures to report.',
            'disclosure_expire_on': timezone.now()             
            }
        response = self.client.post(url, self.author_data)
        self.author_id = response.data['id']

    def test_create_author(self):
        url = reverse('content:author-list')
        data = {
            'title': 'Zubin John Eapen, MD',
            'headline': 'Assistant Professor of Medicine\nMember in the Duke Clinical Research Institute',
            'thumbnails_headline_url': 
            'https://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam',
            'disclosure_statement': 'The author has no industry disclosures to report.',
            'disclosure_expire_on': timezone.now() 
            }
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_author_invalid_url(self):
        url = reverse('content:author-list')
        data = {
            'title': 'Zubin John Eapen, MD',
            'headline': 'Assistant Professor of Medicine\nMember in the Duke Clinical Research Institute',
            'thumbnails_headline_url': 
            'invalid-prefix://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam',
            'disclosure_statement': 'The author has no industry disclosures to report.',
            'disclosure_expire_on': timezone.now() 
            }
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_list_authors(self):
        url = reverse('content:author-list')
        response = self.client.get(url)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_author(self):
        url = reverse('content:author-detail', args=[self.author_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_author(self):
        url = reverse('content:author-detail', args=[self.author_id])
        data =  {
            'title': 'Zubin John Eapen, MD - updated',
            'headline': 'Assistant Professor of Medicine\nMember in the Duke Clinical Research Institute',
            'thumbnails_headline_url': 
            'https://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam',
            'disclosure_statement': 'The author has no industry disclosures to report.',
            'disclosure_expire_on': timezone.now() 
            }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Zubin John Eapen, MD - updated')

    def test_patch_author(self):
        url = reverse('content:author-detail', args=[self.author_id])
        data =  {
            'title': 'Zubin John Eapen, MD - patched',
            'disclosure_statement': 'The author has no industry disclosures to report.',
            'disclosure_expire_on': timezone.now() 
            }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Zubin John Eapen, MD - patched')

    def test_delete_author(self):
        url = reverse('content:author-detail', args=[self.author_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)