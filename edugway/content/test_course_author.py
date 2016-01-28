import json
from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

class CourseTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # set up data for the whole test case 
        pass

    def setUp(self):
        # setup data for each test case
        # create course
        url = reverse('course-list')
        self.course_data = {
            'title': 'A sample course',
            'descr': 'A sample course description ',
            'learning_objective': 'These are the learning objectives for this course'               
            }
        response = self.client.post(url, self.course_data)
        self.course_id = response.data['id']
        # create author
        url = reverse('author-list')
        self.author_data = {
            'title': 'Zubin John Eapen, MD',
            'headline': 'Assistant Professor of Medicine\nMember in the Duke Clinical Research Institute',
            'headline_thumbnail_url': 
            'https://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam',
            'disclosure_statement': 'The author has no industry disclosures to report.',
            'disclosure_expire_on': timezone.now()             
            }
        response = self.client.post(url, self.author_data)
        self.author_id = response.data['id']

    def test_create_course(self):
        url = reverse('course-list')
        data = {
            'title': 'A sample course',
            'descr': 'A sample course description ',
            'learning_objective': 'These are the learning objectives for this course'               
            }
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_courses(self):
        url = reverse('course-list')
        response = self.client.get(url)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course(self):
        url = reverse('course-detail', args=[self.course_id])
        response = self.client.get(url)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course(self):
        url = reverse('course-detail', args=[self.course_id])
        data =  {
            'title': 'A sample course - updated',
            'descr': 'A sample course description',
            'learning_objective': 'These are the learning objectives for this course'               
            }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'A sample course - updated')

    def test_patch_course(self):
        url = reverse('course-detail', args=[self.course_id])
        data =  {
            'title': 'A sample course - patched'              
            }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'A sample course - patched')

    def test_delete_course(self):
        url = reverse('course-detail', args=[self.course_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_course_author(self):
        url = reverse('course-authors', args=[self.course_id])
        data = {'author_id': self.author_id}
        response = self.client.post(url, data)
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # try and create another author for course - should delete existing
        # author and create new relation... only one author relation is allowed...
        data = {'author_id': self.author_id}
        response = self.client.post(url, data)
        print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

