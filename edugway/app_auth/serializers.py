from rest_framework import serializers, validators
from django.contrib.auth import get_user_model
from edugway.utils.serializers import DynamicFieldsModelSerializer

class CurrentUserSerializer(DynamicFieldsModelSerializer):
    username = serializers.CharField(min_length=8, max_length=40,
        validators=[validators.UniqueValidator(queryset=get_user_model().objects.all(),
            message='The username already exists.')])
    first_name = serializers.CharField(max_length=60)
    last_name = serializers.CharField(max_length=60)
    email = serializers.EmailField(max_length=255, 
        validators=[validators.UniqueValidator(queryset=get_user_model().objects.all(),
            message='The email already exists.')])
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
            'new_password', 'confirm_password',  )

    def validate(self, data):
        # verify passwords match.
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if (new_password != confirm_password):
            raise serializers.ValidationError(
                {'confirm_password': 'Confirmation password does not match.'})

        return data
