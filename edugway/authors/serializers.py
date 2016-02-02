from rest_framework import serializers
from django.core import validators as dj_validators
from edugway.authors.models import Author
from edugway.utils.serializers import DynamicFieldsModelSerializer

class AuthorSerializer(DynamicFieldsModelSerializer):
    thumbnails_headline_url = serializers.CharField(write_only=True, 
        validators=[dj_validators.URLValidator()])
    thumbnails = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ('id', 'title', 'headline', 'thumbnails_headline_url', 
            'thumbnails', 'disclosure_statement', 'disclosure_expire_on', )

    # render thumbnails as nested object for consuming clients...
    def get_thumbnails(self, obj):
        return {'headline': {'url': obj.thumbnails_headline_url}}
