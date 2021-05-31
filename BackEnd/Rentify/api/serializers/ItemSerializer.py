from .. import models
from rest_framework import serializers
from .ProductSerializer import ProductSerializer


class ItemSerializer(serializers.ModelSerializer):
    product = serializers.HyperlinkedRelatedField(view_name='product-detail', queryset=models.Product.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=models.Customer.objects.all(), required=False)

    class Meta:
        model = models.Item
        fields = [
            'id',
            'product',
            'customer',
            'quantity',
            'status',
            'start',
            'end',
            'company',
            'duration',
            'check_availability',
            'state',
            'price'
        ]


class BasketSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = models.Basket
        fields = ['items']
