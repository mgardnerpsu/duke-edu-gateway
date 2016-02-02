from django.shortcuts import render
from django.db.models import Max, Min
from rest_framework import mixins, viewsets, serializers, status 
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from edugway.forms.models import Form, Field, Choice
from edugway.forms.serializers import FormSerializer, FormUpdateSerializer, \
                    FieldSerializer, ChoiceSerializer

class FormViewSet(viewsets.ModelViewSet):
    '''
    Forms (assessments, evaluations) resourse actions.
    '''
    queryset = Form.objects.all()
    serializer_class = FormSerializer

    def get_serializer_class(self):
        if self.request.method in ('PUT', 'PATCH'):
            return FormUpdateSerializer
        return self.serializer_class

    @detail_route(methods=['POST', 'GET'])
    def fields(self, request, pk=None):
        if request.method == 'POST':
            form = self.get_object()
            serializer = FieldSerializer(data=request.data, many=False, 
                context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['form'] = form
            max_sequence = form.fields.all().aggregate(
                Max('sequence'))['sequence__max']
            sequence = (1 if (max_sequence is None) else (max_sequence + 1))
            serializer.validated_data['sequence'] = sequence
            serializer.validated_data['name'] = Field.format_name(sequence)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'GET':
            form = self.get_object()
            fields = form.fields
            serializer = FieldSerializer(fields, many=True, 
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

class FieldViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
            mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    Form fields (questions) resourse actions.
    '''
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def perform_destroy(self, instance):
        form = instance.form
        for field in (form.fields.filter(sequence__gt=instance.sequence)):
            field.sequence = field.sequence - 1
            field.name = Field.format_name(field.sequence)
            field.save()
        instance.delete()

    @detail_route(methods=['PUT'], url_path='move-down')
    def move_seq_down(self, request, pk=None):
        field_down = self.get_object()
        form = field_down.form
        max_sequence = form.fields.all().aggregate(
            Max('sequence'))['sequence__max']
        if field_down.sequence == max_sequence:
            # do not move down - this is last field
            pass
        else:
            # swap field positions
            field_up = form.fields.get(sequence=field_down.sequence + 1)
            field_up.sequence = field_up.sequence - 1
            field_up.name = Field.format_name(field_up.sequence)
            field_down.sequence = field_down.sequence + 1 
            field_down.name = Field.format_name(field_down.sequence)
            field_down.save()
            field_up.save()
        serializer = FieldSerializer(field_down, many=False, 
            context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['PUT'], url_path='move-up')
    def move_seq_up(self, request, pk=None):
        field_up = self.get_object()
        form = field_up.form
        min_sequence = form.fields.all().aggregate(
            Min('sequence'))['sequence__min']
        if field_up.sequence == min_sequence:
            # do not move up - this is first field
            pass
        else:
            # swap field positions
            field_down = form.fields.get(sequence=field_up.sequence - 1)
            field_down.sequence = field_down.sequence + 1
            field_down.name = Field.format_name(field_down.sequence)
            field_up.sequence = field_up.sequence - 1 
            field_up.name = Field.format_name(field_up.sequence)
            field_up.save()
            field_down.save()
        serializer = FieldSerializer(field_up, many=False, 
            context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['POST', 'GET'])
    def choices(self, request, pk=None):
        if request.method == 'POST':
            field = self.get_object()
            serializer = ChoiceSerializer(data=request.data, many=False, 
                context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['field'] = field
            max_sequence = field.choices.all().aggregate(
                Max('sequence'))['sequence__max']
            sequence = (1 if (max_sequence is None) else (max_sequence + 1))
            serializer.validated_data['sequence'] = sequence
            serializer.validated_data['name'] = Choice.format_name(sequence)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'GET':
            field = self.get_object()
            choices = field.choices
            serializer = ChoiceSerializer(choices, many=True, 
                context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)

class ChoiceViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
            mixins.DestroyModelMixin, viewsets.GenericViewSet):
    '''
    Field choices (answers) resourse actions.
    '''
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer

    def perform_destroy(self, instance):
        field = instance.field
        for choice in (field.choices.filter(sequence__gt=instance.sequence)):
            choice.sequence = choice.sequence - 1
            choice.name = Choice.format_name(choice.sequence)
            choice.save()
        instance.delete()

    @detail_route(methods=['PUT'], url_path='move-down')
    def move_seq_down(self, request, pk=None):
        choice_down = self.get_object()
        field = choice_down.field
        max_sequence = field.choices.all().aggregate(
            Max('sequence'))['sequence__max']
        if choice_down.sequence == max_sequence:
            # do not move down - this is last choice
            pass
        else:
            # swap choice positions
            choice_up = field.choices.get(sequence=choice_down.sequence + 1)
            choice_up.sequence = choice_up.sequence - 1
            choice_up.name = Choice.format_name(choice_up.sequence)
            choice_down.sequence = choice_down.sequence + 1 
            choice_down.name = Choice.format_name(choice_down.sequence)
            choice_down.save()
            choice_up.save()
        serializer = ChoiceSerializer(choice_down, many=False, 
            context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['PUT'], url_path='move-up')
    def move_seq_up(self, request, pk=None):
        choice_up = self.get_object()
        field = choice_up.field
        min_sequence = field.choices.all().aggregate(
            Min('sequence'))['sequence__min']
        if choice_up.sequence == min_sequence:
            # do not move up - this is first choice
            pass
        else:
            # swap choice positions
            choice_down = field.choices.get(sequence=choice_up.sequence - 1)
            choice_down.sequence = choice_down.sequence + 1
            choice_down.name = Choice.format_name(choice_down.sequence)
            choice_up.sequence = choice_up.sequence - 1 
            choice_up.name = Choice.format_name(choice_up.sequence)
            choice_up.save()
            choice_down.save()
        serializer = ChoiceSerializer(choice_up, many=False, 
            context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['PUT'], url_path='mark-correct')
    def mark_correct(self, request, pk=None):
        correct_choice = self.get_object()
        correct_choice.is_correct = True
        correct_choice.save()
        # for the currently supported field types there can only be 
        # one correct choice... set other choice to incorrect...
        for choice in correct_choice.field.choices.exclude(pk=correct_choice.id):
            choice.is_correct = False
            choice.save()
        serializer = ChoiceSerializer(correct_choice, many=False, 
            context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
