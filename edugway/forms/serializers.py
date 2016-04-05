from rest_framework import serializers
from edugway.forms.models import Form, Field, Choice
from edugway.utils.serializers import DynamicFieldsModelSerializer

class ChoiceSerializer(DynamicFieldsModelSerializer):
    #field = FieldSerializer(many=False, read_only=True, fields=('id',))
    field = serializers.SerializerMethodField()
    sequence = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    # this field is only relevant for forms of type "assessment"
    is_correct = serializers.ReadOnlyField()
   
    class Meta:
        model = Choice
        fields = ('id', 'field', 'sequence', 'name', 'label', 
            'is_correct')

    def get_field(self, obj):
        return {'id': str(obj.field.id)}

class FieldSerializer(DynamicFieldsModelSerializer):
    #form = FormSerializer(many=False, read_only=True, fields=('id',))
    form = serializers.SerializerMethodField()
    sequence = serializers.ReadOnlyField()
    name = serializers.ReadOnlyField()
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Field
        fields = ('id', 'form', 'sequence', 'type', 'name', 
            'label', 'choices')

    def get_form(self, obj):
        return {'id': str(obj.form.id)}

class FormSerializer(DynamicFieldsModelSerializer):
    fields = FieldSerializer(many=True, read_only=True)

    class Meta:
        model = Form
        fields = ('id', 'type', 'title', 'descr', 'fields')

class FormUpdateSerializer(FormSerializer):
    # make type immutable for update (i.e. http put and patch)
    type = serializers.ReadOnlyField()
        