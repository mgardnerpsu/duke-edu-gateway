import collections
from edugway.forms.models import Form, Field, Choice
from rest_framework import serializers

class FormSerializer(serializers.ModelSerializer):
	class Meta:
	    model = Form
	    fields = ('id', 'type', 'title', 'descr')

class FormUpdateSerializer(FormSerializer):
	# make type immutable for update (i.e. http put and patch)
	type = serializers.ReadOnlyField()

class FieldSerializer(serializers.ModelSerializer):
	form = serializers.SerializerMethodField()
	sequence = serializers.ReadOnlyField()
	name = serializers.ReadOnlyField()
   
	class Meta:
	    model = Field
	    fields = ('id', 'form', 'sequence', 'type', 'name', 'label')

	def get_form(self, obj):
		return collections.OrderedDict([('id', str(obj.form.id)), ])

class ChoiceSerializer(serializers.ModelSerializer):
	field = serializers.SerializerMethodField()
	sequence = serializers.ReadOnlyField()
	name = serializers.ReadOnlyField()
   
	class Meta:
	    model = Choice
	    fields = ('id', 'field', 'sequence', 'name', 'label', 'is_correct')

	def get_field(self, obj):
		return collections.OrderedDict([('id', str(obj.field.id)), ])
