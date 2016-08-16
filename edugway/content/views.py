from django.shortcuts import render
from django.db.models import Max, Min
from edugway import settings
from rest_framework import mixins, viewsets, serializers, status 
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from edugway.content.models import Category, Credit, Course, CourseCategory
from edugway.authors.models import Author
from edugway.content.serializers import CategorySerializer, CreditSerializer, \
        CourseSerializer, CourseCategorySerializer, PubCourseSerializer

class CourseViewSet(viewsets.ModelViewSet):
    '''
    Course resourse actions.
    '''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @detail_route(methods=['POST', 'GET'])
    def categories(self, request, pk=None):
        if request.method == 'POST':
            course = self.get_object()
            request.data['course_id'] = course.id
            serializer = CourseCategorySerializer(data=request.data, many=False, 
                context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'GET':
            course = self.get_object()
            categories = course.coursecategory_set.all()
            serializer = CourseCategorySerializer(categories, many=True, 
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['POST', 'GET'])
    def publish(self, request, pk=None):
        if request.method == 'POST':
            course = self.get_object()
            serializer = PubCourseSerializer(data=request.data, many=False, 
                context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['course_id'] = course.id
            max_version = course.pub_courses.all().aggregate(
                Max('version'))['version__max']
            version_number = (1 if (max_version is None) else (max_version + 1))
            serializer.validated_data['version'] = version_number
            # make this published course the current version
            serializer.validated_data['is_current_version'] = True
            for c in course.pub_courses.all():
                c.is_current_version = False
                c.save()
            # get and store snaphot (as JSON) of course version content
            course_response = Response(CourseSerializer(course, many=False,
                context={'request': request}).data, status=status.HTTP_200_OK)
            serializer.validated_data['content_jsonb'] = course_response.data
            serializer.validated_data['content_json'] = course_response.data
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'GET':
            course = self.get_object()
            pub_courses = course.pub_courses.all()
            serializer = PubCourseSerializer(pub_courses, many=True, 
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, 
            viewsets.GenericViewSet):
    '''
    Category resourse actions.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CourseCategoryViewSet(mixins.RetrieveModelMixin, mixins.DestroyModelMixin, 
            viewsets.GenericViewSet):
    '''
    Course categories resourse actions.
    '''
    queryset = CourseCategory.objects.all()
    serializer_class = CourseCategorySerializer

class CreditViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, 
            viewsets.GenericViewSet):
    '''
    Credit resourse actions.
    '''
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer
