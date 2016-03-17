import json
import random
from dateutil.relativedelta import relativedelta
from underscore import _
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
        url = reverse('content:course-list')
        self.course_data = {
            'title': 'A sample course',
            'descr': 'A sample course description ',
            'learning_objective': 'These are the learning objectives for this course'               
            }
        response = self.client.post(url, self.course_data)
        self.course_id = response.data['id']
        # create author
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
        # get category - random selection
        url = reverse('content:category-list')
        response = self.client.get(url)
        self.category_id = random.choice(response.data['results'])['id']
        # get credit - random selection
        url = reverse('content:credit-list')
        response = self.client.get(url)
        self.credit_id = random.choice(response.data['results'])['id']
        # create a video
        url = reverse('content:video-list')
        self.video_data = {
            'provider': Video.PROVIDER_YOUTUBE, 
            'provider_id': self.provider_id
        }
        response = self.client.post(url, self.video_data)
        self.video_id = response.data['id']
        # create a form (assessment)
        url = reverse('content:form-list')
        self.form_data = {'type': Form.TYPE_ASSESSMENT, 'title': 'sample form'}
        response = self.client.post(url, self.form_data)
        self.assessment_id = response.data['id']
        # create a form (evaluation)
        url = reverse('content:form-list')
        self.form_data = {'type': Form.TYPE_EVALUATION, 'title': 'sample form'}
        response = self.client.post(url, self.form_data)
        self.evaluation_id = response.data['id']

    def test_create_course(self):
        url = reverse('content:course-list')
        data = {
            'title': 'A sample course',
            'descr': 'A sample course description ',
            'learning_objective': 'These are the sample learning objectives for this course'         
            }
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_list_courses(self):
        url = reverse('content:course-list')
        response = self.client.get(url)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_course(self):
        url = reverse('content:course-detail', args=[self.course_id])
        response = self.client.get(url)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_course(self):
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {
            'title': 'A sample course - updated',
            'descr': 'A sample course description',
            'learning_objective': 'These are the sample learning objectives for this course'               
            }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'A sample course - updated')

    def test_delete_course(self):
        url = reverse('content:course-detail', args=[self.course_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_associate_course_author(self):
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'author_id': self.author_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_course_category(self):
        # create a course category
        url = reverse('content:course-categories', args=[self.course_id])
        data =  {'category_id': self.category_id}
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # list courses categories
        response = self.client.get(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        course_category_id = response.data[0]['id']
        # get a course category
        url = reverse('content:course-categories-detail', args=[course_category_id])
        response = self.client.get(url)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # delete a course category
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_associate_course_credit(self):
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'credit_id': self.credit_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_course_video(self):
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'video_id': self.video_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_course_assessment(self):
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'assessment_id': self.assessment_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_invalid_assessment_form_type(self):
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'assessment_id': self.evaluation_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_associate_course_evaluation(self):
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'evaluation_id': self.evaluation_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_associate_invalid_evaluation_form_type(self):
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'evaluation_id': self.assessment_id}
        response = self.client.patch(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_publish_course(self):
        # build a course with required content
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'author_id': self.author_id}
        response = self.client.patch(url, data)
        url = reverse('content:course-categories', args=[self.course_id])
        data =  {'category_id': self.category_id}
        response = self.client.post(url, data)
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'credit_id': self.credit_id}
        response = self.client.patch(url, data)
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'video_id': self.video_id}
        response = self.client.patch(url, data)
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'assessment_id': self.assessment_id}
        response = self.client.patch(url, data)
        url = reverse('content:course-detail', args=[self.course_id])
        data =  {'evaluation_id': self.evaluation_id}
        response = self.client.patch(url, data)

        # publish the course several times
        url = reverse('content:course-publish', args=[self.course_id])
        data =  {
            'release_on': timezone.now(),
            'expire_on': timezone.now() + relativedelta(years=1)  
        }
        response = self.client.post(url, data)
        response = self.client.post(url, data)
        response = self.client.post(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # list publishing history
        response = self.client.get(url, data)
        #print(json.dumps(response.data, indent=4))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(_.pluck(response.data, 'version_number'), [3, 2, 1])
        self.assertEqual(_.pluck(response.data, 'is_current_version'), [True, False, False])
