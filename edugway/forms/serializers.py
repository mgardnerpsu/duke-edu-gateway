import collections
from edugway.forms.models import Form, Field
from rest_framework import serializers

class FormSerializer(serializers.ModelSerializer):
	class Meta:
	    model = Form
	    fields = ('id', 'type', 'title', 'descr')

class FormUpdateSerializer(FormSerializer):
	type = serializers.ReadOnlyField()

class FieldSerializer(serializers.ModelSerializer):
	form = serializers.SerializerMethodField()
	number = serializers.ReadOnlyField()
	name = serializers.ReadOnlyField()
	is_required = serializers.ReadOnlyField()
   
	class Meta:
	    model = Field
	    fields = ('id', 'form', 'type', 'number', 'name', 'label', 'is_required')

	def get_form(self, obj):
		return collections.OrderedDict([('id', str(obj.form.id)), ])
