from django.shortcuts import render
from edugway import settings
from rest_framework import mixins, viewsets, serializers, status 
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from edugway.content.models import Category, Credit, Course
from edugway.authors.models import Author
from edugway.content.serializers import CategorySerializer, CreditSerializer, \
        CourseSerializer, CourseAuthorSerializer

class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, 
			viewsets.GenericViewSet):
    '''
    Category resourse actions.
    '''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CreditViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, 
			viewsets.GenericViewSet):
    '''
    Credit resourse actions.
    '''
    queryset = Credit.objects.all()
    serializer_class = CreditSerializer

class CourseViewSet(viewsets.ModelViewSet):
    '''
    Course resourse actions.
    '''
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @detail_route(methods=['POST'])
    def authors(self, request, pk=None):
        if request.method == 'POST':
            course = self.get_object()
            course.courseauthor_set.all().delete()
            request.data['course_id'] = course.id
            serializer = CourseAuthorSerializer(data=request.data, many=False, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
       