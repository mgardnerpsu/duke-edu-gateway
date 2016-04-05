import json
import collections
from rest_framework import serializers, validators
from edugway import settings
from edugway.utils.serializers import DynamicFieldsModelSerializer
from edugway.content.models import Course, PubCourse

class CourseSerializer(DynamicFieldsModelSerializer):
    id = serializers.UUIDField(source='course.id')
    version = serializers.SerializerMethodField()
    title = serializers.CharField(source='content_json.title')
    descr = serializers.CharField(source='content_json.descr')
    learning_objective = serializers.CharField(
        source='content_json.learning_objective')
    author = serializers.JSONField(source='content_json.author')
    categories = serializers.JSONField(source='content_json.categories')
    credit = serializers.JSONField(source='content_json.credit')
    video = serializers.SerializerMethodField()

    class Meta:
        model = PubCourse
        fields = ('id', 'version', 'title', 'descr', 
            'learning_objective', 'author', 'categories', 'credit', 
            'video', )

    def get_video(self, obj):
        video = obj.content_json['video']
        del video['title']
        del video['descr']
        return video

    def get_version(self, obj):
        return collections.OrderedDict([
            ('id', obj.id),
            ('version_number', obj.version),
            ('version_on', obj.version_on),
            ('is_current_version', obj.is_current_version)])
            
