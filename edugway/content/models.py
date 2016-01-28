import uuid
from django.db import models
from django.core import validators as dj_validators
from edugway.authors.models import Author

class Category(models.Model):
    '''
    A category resource that can be associated to a course.
    '''
    class Meta:
        db_table = 'category'
        verbose_name = u'Category'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(u'Label', max_length=60)
    color = models.CharField(u'Hex Color for UX', max_length=20)
    
    def __str__(self):
        return self.label

class Credit(models.Model):
    '''
    A CME credit resource that can be associated to a course.
    '''
    class Meta:
        db_table = 'credit'
        verbose_name = u'CME Credit'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(u'Name', max_length=40)
    label = models.CharField(u'Label', max_length=60)
    descr = models.TextField(u'Description')
    
    def __str__(self):
        return self.label

class Course(models.Model):
    '''
    A course resource and its composite content.
    '''
    class Meta:
        db_table = 'course'
        verbose_name = u'Course'
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(u'Title', max_length=120)
    descr = models.TextField(u'Description')
    learning_objective = models.TextField(u'Learning Objective')
    authors = models.ManyToManyField('authors.Author', through='CourseAuthor')

class CourseAuthor(models.Model):
    '''
    A course author resource - represents association of author to course.
    '''
    class Meta:
        db_table = 'course_author'
        verbose_name = u'Course Author'
        #unique_together = (('course', 'author'),)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, unique=True)     
    author = models.ForeignKey(Author)
