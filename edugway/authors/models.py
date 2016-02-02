import uuid
from django.db import models
from django.core import validators as dj_validators

class Author(models.Model):
    '''
    An author (faculty member) that may be associated to a course.
    '''
    class Meta:
        db_table = 'author'
        verbose_name = u'Author'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(u'Title', max_length=120)
    headline = models.TextField(u'Headline')
    thumbnails_headline_url = models.CharField(u'Headline Thumbnail (portrait) URL', max_length=240,
    	validators=[dj_validators.URLValidator()])
    disclosure_statement = models.TextField(u'Disclosure Summary')
    disclosure_expire_on = models.DateTimeField('Disclosure Expire On')

    def __str__(self):
        return self.title
    