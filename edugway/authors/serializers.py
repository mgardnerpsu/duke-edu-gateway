from edugway.authors.models import Author
from rest_framework import serializers
from django.core import validators as dj_validators

class AuthorSerializer(serializers.ModelSerializer):
    # headline_thumbnail_url = serializers.CharField(write_only=True, 
    #     validators=[dj_validators.URLValidator()])
    # thumbnails = serializers.SerializerMethodField()
    
    class Meta:
        model = Author
        fields = ('id', 'title', 'headline', 'headline_thumbnail_url', # 'thumbnails', 
            'disclosure_statement', 'disclosure_expire_on', )

    # def get_thumbnails(self, obj):
    #     return {'headline': {'url': obj.headline_thumbnail_url}}
