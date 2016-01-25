import collections
import isodate
from edugway.videos.models import Video, YouTube
from rest_framework import serializers

class VideoSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField()
    descr = serializers.SerializerMethodField()
    watch_url = serializers.SerializerMethodField()
    duration = serializers.SerializerMethodField()
    thumbnails = serializers.SerializerMethodField()
    #provider_resource = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = ('id', 'provider', 'provider_id', 'title', 'descr', #'provider_resource'
            'watch_url', 'duration', 'thumbnails', ) 

    def __init__(self, *args, **kwargs):
        super(VideoSerializer, self).__init__(*args, **kwargs)
        self.provider_content = None

    # get the youtube video resource content
    def get_provider_content(self, provider_id):
        if self.provider_content is None:
            #print('calling google get video api')
            self.provider_content = YouTube.get_video(provider_id)
        return self.provider_content

    def get_title(self, obj):
        return self.get_provider_content(obj.provider_id)['snippet']['title']

    def get_descr(self, obj):
        return self.get_provider_content(obj.provider_id)['snippet']['description']

    def get_watch_url(self, obj):
        return YouTube.BASE_WATCH_URL + '/' + obj.provider_id

    def get_duration(self, obj):
        content = self.get_provider_content(obj.provider_id)
        td = isodate.parse_duration(content['contentDetails']['duration'])
        hours, remainder = divmod(td.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return collections.OrderedDict([('hours', hours), ('minutes', minutes), 
            ('seconds', seconds)])

    def get_thumbnails(self, obj):
        return self.get_provider_content(obj.provider_id)['snippet']['thumbnails']

    # def get_provider_resource(self, obj):
    #     return YouTubeVideoSerializer(YouTube.get_video(obj.provider_id)['items'][0]).data

class YouTubeVideoSerializer(serializers.Serializer):
    pass





