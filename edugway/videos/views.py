import collections
from django.shortcuts import render
from django.core.urlresolvers import reverse
from urllib import parse
from rest_framework import mixins, viewsets, serializers, status 
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from edugway import settings
from edugway.videos.models import Video, YouTube
from edugway.videos.serializers import VideoSerializer

class VideoViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, 
            viewsets.GenericViewSet):
    '''
    Video resourse actions.
    '''
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    @list_route(methods=['GET'])
    def youtube(self, request):
        valid_options = ['q', 'maxResults', 'pageToken', 'part', 'type']

        for key in self.request.query_params:
            if key not in valid_options:
                raise serializers.ValidationError(
                    {settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: 
                        ['Invalid query parameter (' + key + ') specified.']})

        options = {}
        options['q'] = self.request.query_params.get('q', None)
        options['maxResults'] = self.request.query_params.get('maxResults', None)
        options['pageToken'] = self.request.query_params.get('pageToken', None)

        if options.get('q') is None:
            raise serializers.ValidationError(
                {settings.REST_FRAMEWORK['NON_FIELD_ERRORS_KEY']: 
                    ['Query term parameter (q) is required.']})

        if options.get('maxResults') is None:
            options['maxResults'] = settings.YOUTUBE_MAX_RESULTS

        if options.get('pageToken') is None:
            del options['pageToken']

        videos = YouTube.search_videos(options)
        
        next_page_token = videos.get('nextPageToken', None)
        prev_page_token = videos.get('prevPageToken', None)
        base_url = reverse('video-youtube')

        count = videos['pageInfo']['totalResults']

        results_per_page = videos['pageInfo']['resultsPerPage']

        next_url = None
        if next_page_token is not None:
            options['pageToken'] = next_page_token
            next_url = request.build_absolute_uri(base_url + '?' + parse.urlencode(options))

        prev_url = None
        if prev_page_token is not None:
            options['pageToken'] = prev_page_token
            prev_url = request.build_absolute_uri(base_url + '?' + parse.urlencode(options))

        results = videos['items']

        videos = collections.OrderedDict([
            ('count', count), ('next', next_url), ('previous', prev_url), 
            ('results_per_page', results_per_page), ('results', results)])

        return Response(videos, status.HTTP_200_OK)
