import uuid
from django.db import models
from django.core import validators as dj_validators

class Author(models.Model):
    '''
    An author (faculty) resource that may be associated to a course.
    '''
    class Meta:
        db_table = 'author'
        verbose_name = u'Author'

    title = models.CharField(u'Title', max_length=240)
    headline = models.TextField(u'Headline')
    headline_thumbnail_url = models.CharField(u'Headline Portrait URL', max_length=240,
    	validators=[dj_validators.URLValidator()])
    disclosure_statement = models.TextField(u'Disclosure Summary', blank=True)
    disclosure_expire_on = models.DateTimeField('Disclosure Expire On', null=True)

    def __str__(self):
        return self.title
    