import uuid
from django.db import models
from django.core import validators as dj_validators

class Category(models.Model):
    '''
    A category resource that can be associated to a course.
    '''
    class Meta:
        db_table = 'category'
        verbose_name = u'Category'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    label = models.CharField(u'Label', max_length=50)
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
    label = models.CharField(u'Label', max_length=50)
    descr = models.TextField(u'Description')
    
    def __str__(self):
        return self.label

# class Course(models.Model):
# 	pass
