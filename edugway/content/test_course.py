import json
import random
from django.core.urlresolvers import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase
from edugway.videos.models import Video, YouTube
from edugway.forms.models import Form

class CourseTests(APITestCase):
    # load required fixtures
    fixtures = ['category', 'credit', ]

    @classmethod
    def setUpTestData(cls):
        # set up data for the whole test case
        cls.yt = YouTube.get_service()
        cls.provider_id = 'r10kqd1HDCI' 

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
            'thumbnails_headline_url': 
            'https://medicine.duke.edu/sites/medicine.duke.edu/files/styles/profile/public/i1638962?itok=Ti3sFdam',
            'disclosure_statement': 'The author has no industry disclosures to report.',
            'disclosure_expire_on': timezone.now()             
            }
        response = self.client.post(url, self.author_data)
        self.author_id = response.data['id']
        # get category - random selection
        url = reverse('category-list')
        response = self.client.get(url)
        self.category_id = random.choice(response.data['results'])['id']
        # get credit - random selection
        url = reverse('credit-list')
        response = self.client.get(url)
        self.credit_id = random.choice(response.data['results'])['id']
        # create a video
        url = reverse('video-list')
        self.video_data = {
            'provider': Video.PROVIDER_YOUTUBE, 
            'provider_id': self.provider_id
        }
        response = self.client.post(url, self.video_data)
        self.video_id = response.data['id']
        # create a form (assessment)
        url = reverse('form-list')
        self.form_data = {'type': Form.TYPE_ASSESSMENT, 'title': 'sample form'}
        response = self.client.post(url, self.form_data)
        self.assessment_id = response.data['id']
        # create a form (evaluation)
        url = reverse('form-list')
        self.form_data = {'type': Form.TYPE_EVALUATION, 'title': 'sample form'}
        response = self.client.post(url, self.form_data)
        self.evaluation_id = response.data['id']

    def test_create_course(self):
        url = reverse('course-list')
        data = {
            'title': 'A sample course',
            'descr': 'A sample course description ',
            'learning_objective': 'These are the sample learning objectives for this course'         
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

    def test_delete_course(self):
        url = reverse('course-detail', args=[self.course_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_associate_course_author(self):
        url = reverse('course-detail', args=[self.course_id])
        data =  {'author_id': self.author_id}
        response = self.client.patch(url, data)
        #sprint(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_course_category(self):
        url = reverse('course-detail', args=[self.course_id])
        data =  {'category_id': self.category_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_course_credit(self):
        url = reverse('course-detail', args=[self.course_id])
        data =  {'credit_id': self.credit_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_course_video(self):
        url = reverse('course-detail', args=[self.course_id])
        data =  {'video_id': self.video_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_course_assessment(self):
        url = reverse('course-detail', args=[self.course_id])
        data =  {'assessment_id': self.assessment_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_invalid_assessment_form_type(self):
        url = reverse('course-detail', args=[self.course_id])
        data =  {'assessment_id': self.evaluation_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_associate_course_evaluation(self):
        url = reverse('course-detail', args=[self.course_id])
        data =  {'evaluation_id': self.evaluation_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_invalid_evaluation_form_type(self):
        url = reverse('course-detail', args=[self.course_id])
        data =  {'evaluation_id': self.assessment_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # These test cases may be relevant if it is determined post-alpha that
    # we need to support more than one author per course...
    # def test_create_course_author(self):
    #     url = reverse('course-authors', args=[self.course_id])
    #     data = {'author_id': self.author_id}
    #     response = self.client.post(url, data)
    #     #print(json.dumps(response.data, indent=4))
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     # try and create another author for course - should delete existing
    #     # author and create new relation... only one author relation is allowed...
    #     data = {'author_id': self.author_id}
    #     response = self.client.post(url, data)
    #     #print(json.dumps(response.data, indent=4))
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_list_course_authors(self):
    #     # create the course author
    #     url = reverse('course-authors', args=[self.course_id])
    #     data = {'author_id': self.author_id}
    #     response = self.client.post(url, data)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     # lists the course author
    #     url = reverse('course-authors', args=[self.course_id])
    #     response = self.client.get(url)
    #     print(json.dumps(response.data, indent=4))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

