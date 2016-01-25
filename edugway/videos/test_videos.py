import json
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from edugway.videos.models import Video, YouTube

class VideoTests(APITestCase):
	@classmethod
	def setUpTestData(cls):
		# set up data for the whole test case
		cls.yt = YouTube.get_service()
		cls.provider_id = 'r10kqd1HDCI' 

	def setUp(self):
		# setup data for each test case
		url = reverse('video-list')
		self.video_data = {'provider': Video.PROVIDER_YOUTUBE, 'provider_id': self.provider_id}
		response = self.client.post(url, self.video_data)
		self.video_id = response.data['id']

	def test_create_video(self):
		url = reverse('video-list')
		video_data = {'provider': Video.PROVIDER_YOUTUBE,  'provider_id': 'XUaqnxHn-QY'}
		response = self.client.post(url, video_data)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_duplicate_video(self):
		url = reverse('video-list')
		video_data = {'provider': Video.PROVIDER_YOUTUBE,  'provider_id': 'r10kqd1HDCI'}
		response = self.client.post(url, video_data)
		print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_list_videos(self):
		url = reverse('video-list')
		response = self.client.get(url)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_get_video(self):
		url = reverse('video-detail', args=[self.video_id])
		response = self.client.get(url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_search_ytube_videos(self):
		url = reverse('video-youtube')
		# verify 'q' search parameter is required
		response = self.client.get(url)
		print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		# verify invalid search params not accepted
		response = self.client.get(url, {'bad_param': 'bad_value'})
		print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		# verify valid query works
		response = self.client.get(url, {'q':'Duke Education Gateway', 'maxResults': 5})
		self.assertEqual(len(response.data['results']), 5)
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		# verify we can get the next page
		response = self.client.get(response.data['next'])
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_200_OK)	
		# verify we can get the previous page
		response = self.client.get(response.data['previous'])
		#print(json.dumps(response.data, indent=4))
		self.assertEqual(response.status_code, status.HTTP_200_OK)		

	

