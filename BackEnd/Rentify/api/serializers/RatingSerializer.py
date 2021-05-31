from .. import models
from rest_framework import serializers


class RatingsSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    product = serializers.StringRelatedField()

    class Meta:
        model = models.Rating
        fields = ['id', 'user', 'product', 'stars']
        required = ['stars']
