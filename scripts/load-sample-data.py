#!/usr/bin/env python
import os, sys
# configure django settings... and bootstrap django
sys.path.append('./')
#sys.path.append('../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edugway.settings')
import django
django.setup()

import random, json
from dateutil.relativedelta import relativedelta
from underscore import _
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.core.management import call_command
from rest_framework import status
from rest_framework.test import APIClient
from edugway.forms.models import Form, Field, Choice
from edugway.authors.models import Author
from edugway.videos.models import Video, YouTube
from edugway.content.models import Course, Category, Credit

'''
Clear all database content...
'''
call_command('flush')

# create API client handle
client = APIClient()

'''
First we will create some sample reference data...
'''
# create sample assessment/evaluation forms
form_title_base = 'A sample form for testing Little Green Web portal.' 
field_label_base = 'This question content is for testing ' + \
    'of the Little Green Web portal?'
choice_label_base = 'This is answer content for testing ' + \
    'of the Little Green Web portal.'

# create the form
for x in range(1, 51):
    url = reverse('form-list')
    data = {
        'type': random.choice([Form.TYPE_ASSESSMENT, Form.TYPE_EVALUATION]),
        'title': form_title_base
        }
    response = client.post(url, data)
    assert (response.status_code == 201)
    form_id = response.data['id']
    # create some fields (questions)
    for x in range(1, 6):
        url = reverse('form-fields', args=[form_id])
        data = {
            'type': random.choice([Field.TYPE_RADIO, Field.TYPE_DROPDOWN]),
            'label': field_label_base
            }
        response = client.post(url, data)
        assert (response.status_code == 201)
        field_id = response.data['id']
        # create some choices (answers)
        for x in range(1, 5):
            url = reverse('form-fields-choices', args=[field_id])
            data = {
                'label': choice_label_base
                }
            response = client.post(url, data)
            assert (response.status_code == 201)
           
# set a random correct answer for assessment forms
for field in Field.objects.filter(form__type=Form.TYPE_ASSESSMENT):
    choice = random.choice(field.choices.all())
    url = reverse('field-choices-mark-correct', args=[choice.id])
    response = client.put(url)
    assert (response.status_code == 200)
    url = reverse('field-choices-detail', args=[choice.id])
    response = client.patch(url, data={'label': choice.label + ' [correct choice]'})
    assert (response.status_code == 200)

# load sample authors from the "pre-alpha" release
author_baseline_disclosure = 'A sample disclosure for testing Little Green Web portal' + \
    '; this sample author has the following industry disclosures to report: \n' + \
    '1. Author holds shares of common stock in Little Green Software.\n' + \
    '2. Author holds shares of preferred stock in Education Enterprises, Inc.'
with open('./scripts/author.json') as author_data:
    authors = json.load(author_data)
    for author in authors:
        author = author['fields']
        url = reverse('author-list')
        data = {
            'title': author['title'],
            'headline': author['headline'],
            'thumbnails_headline_url': author['thnail_feature_url'],
            'disclosure_statement': author_baseline_disclosure,
            'disclosure_expire_on': timezone.now() + relativedelta(years=1)        
            }
        if data['thumbnails_headline_url'] is None:
            data['thumbnails_headline_url'] = 'https://invalid-image-url.jpg'
        response = client.post(url, data)
        assert (response.status_code == 201)

# load sample videos from the "Duke Education Gateway" 
# only load videos from these channels... 
channel_ids = (
    'UCm8DRqjkykFsX941iJFSSig', # Duke Clinical Research Institute
    'UCNhXTS_yLO9HgFuiQuhf2AA' # Duke Health
    )

url = reverse('video-youtube')
response = client.get(url, {'q': '', 'channelId': 'UCm8DRqjkykFsX941iJFSSig'})
assert (response.status_code == 200)

next_page = True
while next_page:

    for yt_video in response.data['results']:
        url = reverse('video-list')
        data = {
            'provider': Video.PROVIDER_YOUTUBE,  
            'provider_id': yt_video['id']['videoId']
            }
        dup_response = client.get(url, data)
        assert (dup_response.status_code == 200)
        # if video does not exist - then create video
        if dup_response.data['count'] == 0:
            create_response = client.post(url, data)
            assert (create_response.status_code == 201)

    next_page_url = response.data['next']
    if next_page_url is not None:
        response = client.get(next_page_url)
        assert (response.status_code == 200)
        next_page = True
    else:
        next_page = False

# load category and credit fixtures
call_command('loaddata', 'category')
call_command('loaddata', 'credit')

'''
Build sample courses based on videos and sample reference data...
'''
course_baseline_learning_objective = 'Sample learning objectives for testing Little Green Web portal' + \
    '; after completing this course you should understand the following: \n' + \
    '1. How login to the education gateway and search for courses.\n' + \
    '2. How to take a course and complete all course components.\n' + \
    '3. How to email a copy of your course certificate.'

for video in Video.objects.all():
    # create the course
    yt_video = YouTube.get_video(video.provider_id)
    data = {
        'title': yt_video['snippet']['title'], 
        'descr': yt_video['snippet']['description'],
        'learning_objective': course_baseline_learning_objective
    }
    if not data['descr'].strip():
        data['descr'] = 'A sample course description for testing the Little Green Web portal.'
    url = reverse('course-list')
    response = client.post(url, data)
    assert (response.status_code == 201)
    id = response.data['id']
    # associate reference content
    url = reverse('course-detail', args=[id])
    data = {'author_id': random.choice(Author.objects.all()).id}
    response = client.patch(url, data)
    assert (response.status_code == 200)
    data = {'category_id': random.choice(Category.objects.all()).id}
    response = client.patch(url, data)
    assert (response.status_code == 200)
    data = {'credit_id': random.choice(Credit.objects.all()).id}
    response = client.patch(url, data)
    assert (response.status_code == 200)
    data = {'video_id': random.choice(Video.objects.all()).id}
    response = client.patch(url, data)
    assert (response.status_code == 200)
    data = {'assessment_id': random.choice(Form.objects.filter(type='assessment')).id}
    response = client.patch(url, data)
    assert (response.status_code == 200)
    data = {'evaluation_id': random.choice(Form.objects.filter(type='evaluation')).id}
    response = client.patch(url, data)
    assert (response.status_code == 200)

