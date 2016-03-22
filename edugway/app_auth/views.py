from django.shortcuts import render
from django.contrib.auth import get_user_model
from edugway import settings
from rest_framework import mixins, viewsets, serializers, status 
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from edugway.app_auth.serializers import CurrentUserSerializer

class CurrentUserViewSet(viewsets.GenericViewSet):
    '''
    Current user resource actions (including user registration).
    '''
    queryset = get_user_model().objects.all()
    serializer_class = CurrentUserSerializer

    @list_route(methods=['POST'], permission_classes=[])
    def register(self, request):
        serializer = CurrentUserSerializer(data=request.data, many=False, 
                context={'request': request})
        serializer.is_valid(raise_exception=True)
        # remove the temporary passwoed fields...
        password = serializer.validated_data['new_password']
        del serializer.validated_data['new_password']
        del serializer.validated_data['confirm_password']
        serializer.save()
        serializer.instance.set_password(password)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
