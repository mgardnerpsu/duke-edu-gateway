import collections
from rest_framework import serializers, validators
from edugway import settings
from edugway.content.models import Category, Credit, Course
from edugway.forms.models import Form
from edugway.authors.serializers import AuthorSerializer
from edugway.videos.serializers import VideoSerializer
from edugway.forms.serializers import FormSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label', 'color', ) 

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ('id', 'label', 'descr', ) 

class CourseSerializer(serializers.ModelSerializer):
    author_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    category_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    credit_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    video_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    assessment_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    evaluation_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    author = AuthorSerializer(many=False, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    credit = CreditSerializer(many=False, read_only=True)
    video = VideoSerializer(many=False, read_only=True)
    assessment = FormSerializer(many=False, read_only=True)
    evaluation = FormSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'descr', 'learning_objective', 'author_id', 'author', 
            'category_id', 'category', 'credit_id', 'credit', 'video_id', 'video',
            'assessment_id', 'assessment', 'evaluation_id', 'evaluation', )

    def validate(self, data):
        # verify form type relations are valid.
        assessment_id = data.get('assessment_id', None)
        evaluation_id = data.get('evaluation_id', None)

        if assessment_id is not None:
            try:
                Form.objects.get(pk=assessment_id, type=Form.TYPE_ASSESSMENT)
            except Form.DoesNotExist:
                raise serializers.ValidationError(
                    'Invalid form type specified for a course assessment.')

        if evaluation_id is not None:
            try:
                Form.objects.get(pk=evaluation_id, type=Form.TYPE_EVALUATION)
            except Form.DoesNotExist:
                raise serializers.ValidationError(
                    'Invalid form type specified for a course evaluation.')

        return data
 