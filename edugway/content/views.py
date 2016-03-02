from django.shortcuts import render
from edugway import settings
from rest_framework import mixins, viewsets, serializers, status 
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from edugway.content.models import Category, Credit, Course, CourseCategory
from edugway.authors.models import Author
from edugway.content.serializers import CategorySerializer, CreditSerializer, \
        CourseSerializer, CourseCategorySerializer

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
    Course categories (questions) resourse actions.
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


       