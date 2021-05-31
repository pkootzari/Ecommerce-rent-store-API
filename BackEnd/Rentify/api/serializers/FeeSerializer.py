from .. import models
from rest_framework import serializers


class FeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Fee
        fields = ['id', 'time_unit', 'amount', 'price']
