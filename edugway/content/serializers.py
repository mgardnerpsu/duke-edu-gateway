import collections
from edugway import settings
from edugway.content.models import Category, Credit, Course, \
        CourseAuthor
from rest_framework import serializers, validators

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label', 'color', ) 

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ('id', 'label', 'descr', ) 

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'title', 'descr', 'learning_objective', )

class CourseAuthorSerializer(serializers.ModelSerializer):
    course_id = serializers.CharField(write_only=True)
    author_id = serializers.CharField(write_only=True)
    course = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()

    validators = [
            validators.UniqueTogetherValidator(
                queryset=CourseAuthor.objects.all(),
                fields=('course_id', ),
                message='An author has already been associated to this course.'
            )
        ]

    class Meta:
        model = CourseAuthor
        fields = ('id', 'course_id', 'author_id', 'course', 'author', )

    def get_course(self, obj):
        return collections.OrderedDict([('id', str(obj.course.id)), ])

    def get_author(self, obj):
        return collections.OrderedDict([('id', str(obj.author.id)), ])
 
 