import uuid
from django.db import models
from edugway.authors.models import Author
from edugway.videos.models import Video
from edugway.forms.models import Form

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
    author = models.ForeignKey(Author, on_delete=models.PROTECT, null=True)
    credit = models.ForeignKey('content.Credit', on_delete=models.PROTECT, null=True)
    video = models.ForeignKey(Video, on_delete=models.PROTECT, null=True)
    assessment = models.ForeignKey(Form, on_delete=models.PROTECT, null=True, 
        choices=[(f.id, f.title) for f in Form.objects.filter(type=Form.TYPE_ASSESSMENT)],
        related_name='assessment', )
    evaluation = models.ForeignKey(Form, on_delete=models.PROTECT, null=True,
        choices=[(f.id, f.title) for f in Form.objects.filter(type=Form.TYPE_EVALUATION)],
        related_name='evaluation')

class Category(models.Model):
    '''
    A category resource that can be associated to a course.
    '''
    class Meta:
        db_table = 'category'
        verbose_name = u'Category'
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(u'Name', max_length=40)
    label = models.CharField(u'Label', max_length=60)
    color = models.CharField(u'Hex Color for UX', max_length=20)
    
    def __str__(self):
        return self.label

class CourseCategory(models.Model):
    '''
    A course category represents an association of a category to a course.
    '''
    class Meta:
        db_table = 'course_category'
        verbose_name = u'Course Category'
        unique_together = (('course', 'category'),)
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course)    
    category = models.ForeignKey(Category)

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
