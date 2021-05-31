from .. import models
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']


class SubCategorySerializer(serializers.ModelSerializer):
    parent_category = CategorySerializer()

    class Meta:
        fields = ['id', 'name', 'parent_category']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name']
