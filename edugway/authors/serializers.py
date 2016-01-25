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

    def validate(self, data):
        # verify disclosure expiration date is provided with disclosure statement.
        disclosure_statement = data.get('disclosure_statement', '').strip()
        disclosure_expire_on = data.get('disclosure_expire_on', None)
        if (disclosure_statement and not disclosure_expire_on):
            raise serializers.ValidationError('Must specify disclosure expire date.')
        # if no disclosure exists then set expire date to null
        if (not disclosure_statement):
            data['disclosure_expire_on'] = None
        return data

