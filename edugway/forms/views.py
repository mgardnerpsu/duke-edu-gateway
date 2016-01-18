from django.shortcuts import render
from django.db.models import Max
from rest_framework import generics, mixins, viewsets, serializers, status 
from rest_framework.decorators import api_view, detail_route, list_route
from rest_framework.response import Response
from edugway.forms.models import Form, Field
from edugway.forms.serializers import FormSerializer, FormUpdateSerializer, FieldSerializer

class FormViewSet(viewsets.ModelViewSet):
	'''
	Forms (assessment, evaluation) resourse actions
	'''
	queryset = Form.objects.all()
	serializer_class = FormSerializer

	def get_serializer_class(self):
		if self.request.method in ('PUT', 'PATCH'):
			return FormUpdateSerializer
		return self.serializer_class

	def create_form_field(data={}):
		pass

	@detail_route(methods=['POST', 'GET'])
	def fields(self, request, pk=None):
		if request.method == 'POST':
			form = self.get_object()
			serializer = FieldSerializer(data=request.data, many=False, context={'request': request})
			serializer.is_valid(raise_exception=True)
			serializer.validated_data['form'] = form
			max_number = form.fields.all().aggregate(Max('number'))['number__max']
			number = (1 if (max_number is None) else (max_number + 1))
			serializer.validated_data['number'] = number
			serializer.validated_data['name'] = 'field-' + str(number)
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		if request.method == 'GET':
			form = self.get_object()
			fields = form.fields
			serializer = FieldSerializer(fields, many=True, context={'request': request})
			return Response(serializer.data, status=status.HTTP_200_OK)

class FieldViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
			mixins.DestroyModelMixin, viewsets.GenericViewSet):
	'''
	Fields resourse actions
	'''
	queryset = Field.objects.all()
	serializer_class = FieldSerializer
