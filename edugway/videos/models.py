import uuid
import collections
from django.db import models
from django.contrib.postgres.fields import JSONField
# include google API apiclient resources
from apiclient.discovery import build
from apiclient.errors import HttpError as gooleApiHttpError
from edugway import settings

class Video(models.Model):
    '''
    A video that may be associated to a course.
    '''
    class Meta:
        db_table = 'video'
        verbose_name = u'Video'
        unique_together = (('provider', 'provider_id'),)

    PROVIDER_YOUTUBE = u'youtube'
    PROVIDER_VIMEO = u'vimeo'
    
    PROVIDER_CHOICES = (
        (PROVIDER_YOUTUBE, u'YouTube'),
        (PROVIDER_VIMEO, u'Vimeo'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(u'Provider', max_length=50, choices=PROVIDER_CHOICES)
    provider_id = models.CharField(u'Provider ID', max_length=50)
    provider_resource = JSONField()

    def __str__(self):
        return self.provider

class YouTube:
    '''
    A TouTube video that may be associated to a course; this is an application
    level wrapper for the Google YouTube API video resource content.
    '''
    # create the youtube class level service handle
    youtube = build(settings.YOUTUBE_API_SERVICE_NAME, settings.YOUTUBE_API_VERSION,           
        developerKey=settings.YOUTUBE_API_KEY)

    @classmethod
    def get_service(cls):
        return cls.youtube

    @classmethod
    def search_videos(cls, options):
        options['type'] = 'video'
        options['part'] = 'id, snippet'
        yt = cls.get_service()
        return yt.search().list(**options).execute()

    @classmethod
    def get_video(cls, id):
        yt = cls.get_service()
        return yt.videos().list(id=id, maxResults=1, 
            part='id, snippet, contentDetails, player').execute()['items'][0]

