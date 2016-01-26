from edugway.content.models import Category, Credit
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'label', 'color', ) 

class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields = ('id', 'label', 'descr', ) 
