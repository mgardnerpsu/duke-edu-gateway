import uuid
from django.db import models

class Form(models.Model):
    '''
    A form and its composite models contain the metadata (fields, field coices, etc.) 
    required to define an assessment/evaluation that may be associated to a course.
    '''
    class Meta:
    	db_table = 'form'
    	verbose_name = u'Form'

    TYPE_ASSESSMENT = u'assessment'
    TYPE_EVALUATION = u'evaluation'
    
    TYPE_CHOICES = (
        (TYPE_ASSESSMENT, u'Assessment'),
        (TYPE_EVALUATION, u'Evaluation'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(u'Type', max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(u'Title', max_length=100)
    descr = models.TextField(u'Description', blank=True)

    def __str__(self):
        return self.title

class Field(models.Model):
    '''
    A field (question) contained within a form.
    '''
    class Meta:
        db_table = 'field'
        verbose_name = u'Form Field'
        ordering = ('form', 'sequence')
        
    TYPE_RADIO = u'multi-choice-radio'
    TYPE_DROPDOWN = u'multi-choice-dropdown'
    
    TYPE_CHOICES = (
        (TYPE_RADIO, u'Multiple Choice - Single Answer (Radio Buttons)'),
        (TYPE_DROPDOWN, u'Multiple Choice - Single Answer (Drop-down List)')
    )

    CHOICE_TYPES = (TYPE_RADIO, TYPE_DROPDOWN, )
    SINGLE_CHOICE_TYPES = (TYPE_RADIO, TYPE_DROPDOWN, )     
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form = models.ForeignKey(Form, related_name=u'fields')
    sequence = models.IntegerField(u'Display Sequence')
    type = models.CharField(u'Type', max_length=50, choices=TYPE_CHOICES)
    name = models.CharField(u'Field Name', max_length=50)
    label = models.TextField(u'Label (Question)')

    @classmethod
    def format_name(cls, sequence):
    # Generate name using default prefix   
        return 'field-' + str(sequence)

    def __str__(self):
        return self.label

class Choice(models.Model):
    '''
    A choice (answer) for a field (question).
    '''
    class Meta:
        db_table = 'choice'
        verbose_name = u'Field Choice'
        ordering = ('field', 'sequence')
     
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    field = models.ForeignKey(Field, related_name='choices')
    sequence = models.IntegerField(u'Display Sequence')
    name = models.CharField(u'Choice Name', max_length=50)
    label = models.TextField(u'Label (Answer)')
    is_correct = models.BooleanField('Correct Choice?', default=False)

    @classmethod
    def format_name(cls, sequence):
    # Generate name using default prefix   
        return 'choice-' + str(sequence)

    def __str__(self):
        return self.label
