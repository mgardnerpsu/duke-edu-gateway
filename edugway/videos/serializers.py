import collections
import isodate
from underscore import _
from rest_framework import serializers, validators
from edugway import settings
from edugway.videos.models import Video, YouTube
from edugway.utils.serializers import DynamicFieldsModelSerializer

class VideoSerializer(DynamicFieldsModelSerializer):
    title = serializers.SerializerMethodField()
    descr = serializers.SerializerMethodField()
    watch_url = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    
    class Meta:
        model = Video
        fields = ('id', 'provider', 'provider_id', 'title', 'descr', 
                'watch_url', 'duration', 'thumbnails', ) 

    validators = [
            validators.UniqueTogetherValidator(
                queryset=Video.objects.all(),
                fields=('provider', 'provider_id', ),
                message='The provider (YouTube, Vimeo, etc.) video already exists.'
            )
        ]

    def get_title(self, obj):
        return obj.provider_resource['snippet']['title']

    def get_descr(self, obj):
        return obj.provider_resource['snippet']['description']

    def get_watch_url(self, obj):
        return settings.YOUTUBE_BASE_WATCH_URL + '/' + obj.provider_id

    def get_duration(self, obj):
        td = isodate.parse_duration(obj.provider_resource['contentDetails']['duration'])
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return collections.OrderedDict([('hours', hours), ('minutes', minutes), 
            ('seconds', seconds)])

    def get_thumbnails(self, obj):
        return obj.provider_resource['snippet']['thumbnails']

