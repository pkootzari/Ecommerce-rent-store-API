from .. import models
from rest_framework import serializers
from ..serializers import ProductSerializer, CustomerSerializer


# class InvoiceDetailSerializer(serializers.ModelSerializer):
#     products = serializers.SerializerMethodField('products_list')
#     customer = serializers.SerializerMethodField('customer_detail')
#
#     def products_list(self, obj):
#         return ProductSerializer(obj.cart.products.all(), many=True).data
#
#     def customer_detail(self, obj):
#         return CustomerSerializer(obj.cart.customer).data
#
#     class Meta:
#         model = models.Invoice
#         fields = ['customer', 'products', 'total_price', 'discount', 'tax', 'order_price']
