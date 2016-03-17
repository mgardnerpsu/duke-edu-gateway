import json
import collections
from rest_framework import serializers, validators
from edugway import settings
from edugway.utils.serializers import DynamicFieldsModelSerializer
from edugway.content.models import Course, PubCourse

class CourseSerializer(DynamicFieldsModelSerializer):

    version_on = serializers.DateTimeField(
            source='current_version.version_on')
    version_number = serializers.IntegerField(
            source='current_version.version_number')
    content = serializers.SerializerMethodField()

    class Meta:
        model = PubCourse
        fields = ('id', 'version_on', 'version_number', 'content', )

    def get_content(self, obj):
        author = obj.current_version.content_json['author']
        video = obj.current_version.content_json['video']
        del video['title']
        del video['descr']
        assessment = obj.current_version.content_json['assessment']
        assessment = {'id': assessment['id']}
        evaluation = obj.current_version.content_json['evaluation']
        evaluation = {'id': evaluation['id']}
        return collections.OrderedDict([
            ('author', author),
            ('video', video), 
            ('assessment', assessment),
            ('evaluation', evaluation),
        ])
