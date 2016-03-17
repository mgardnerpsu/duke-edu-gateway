import collections
from rest_framework import serializers, validators
from edugway import settings
from edugway.content.models import Category, Credit, Course, \
        CourseCategory, PubCourse
from edugway.forms.models import Form
from edugway.authors.serializers import AuthorSerializer
from edugway.videos.serializers import VideoSerializer
from edugway.forms.serializers import FormSerializer
from edugway.utils.serializers import DynamicFieldsModelSerializer

class CategorySerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label', 'color', ) 

class CreditSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Credit
        fields = ('id', 'label', 'descr', ) 

class CourseSerializer(DynamicFieldsModelSerializer):
    author_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    credit_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    video_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    assessment_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    evaluation_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)
    author = AuthorSerializer(many=False, read_only=True)
    categories = serializers.SerializerMethodField()
    credit = CreditSerializer(many=False, read_only=True)
    video = VideoSerializer(many=False, read_only=True)
    assessment = FormSerializer(many=False, read_only=True)
    evaluation = FormSerializer(many=False, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'descr', 'learning_objective', 'author_id', 'author', 
            'categories', 'credit_id', 'credit', 'video_id', 'video',
            'assessment_id', 'assessment', 'evaluation_id', 'evaluation', )

    def get_categories(self, obj):         
        categories = obj.coursecategory_set.all()    
        serializer = CourseCategorySerializer(categories, many=True, context=self.context)
        return serializer.data

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

class CourseCategorySerializer(DynamicFieldsModelSerializer):
    course_id = serializers.UUIDField(write_only=True)
    category_id = serializers.UUIDField(write_only=True)
    course = serializers.SerializerMethodField()
    category = CategorySerializer(many=False, read_only=True)

    validators = [
        validators.UniqueTogetherValidator(
         queryset=CourseCategory.objects.all(),
         fields=('course_id', 'category_id', ),
         message='The specified category has already been associated to this course.'
        )
    ]
    
    class Meta:
        model = CourseCategory
        fields = ('id', 'course_id', 'course', 'category_id', 'category', ) 

    def get_course(self, obj):
        return {'id': str(obj.course.id)}

class PubCourseSerializer(DynamicFieldsModelSerializer):
    course = serializers.SerializerMethodField()
    version_number = serializers.ReadOnlyField()
    version_on = serializers.DateTimeField(read_only=True)
    is_current_version = serializers.ReadOnlyField()
    content_jsonb = serializers.JSONField(read_only=True)
    content_json = serializers.JSONField(read_only=True)
    
    class Meta:
        model = PubCourse
        fields = ('id', 'course', 'version_number', 'version_on',
            'is_current_version', 'release_on', 'expire_on', 
            'content_jsonb', 'content_json', )

    def get_course(self, obj):
        return {'id': str(obj.course.id)}
 