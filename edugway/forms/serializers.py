from rest_framework import serializers
from edugway.forms.models import Form, Field, Choice
from edugway.utils.serializers import DynamicFieldsModelSerializer

class FormSerializer(DynamicFieldsModelSerializer):
	class Meta:
	    model = Form
	    fields = ('id', 'type', 'title', 'descr')

class FormUpdateSerializer(FormSerializer):
	# make type immutable for update (i.e. http put and patch)
	type = serializers.ReadOnlyField()

class FieldSerializer(DynamicFieldsModelSerializer):
	form = FormSerializer(many=False, read_only=True, fields=('id',))
	sequence = serializers.ReadOnlyField()
	name = serializers.ReadOnlyField()
   
	class Meta:
	    model = Field
	    fields = ('id', 'form', 'sequence', 'type', 'name', 'label')

class ChoiceSerializer(DynamicFieldsModelSerializer):
	field = FieldSerializer(many=False, read_only=True, fields=('id',))
	sequence = serializers.ReadOnlyField()
	name = serializers.ReadOnlyField()
	# this field is only relevant for forms of type "assessment"
	is_correct = serializers.ReadOnlyField()
   
	class Meta:
	    model = Choice
	    fields = ('id', 'field', 'sequence', 'name', 'label', 'is_correct')
		