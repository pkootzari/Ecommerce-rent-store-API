from .. import models
from rest_framework import serializers
from ..serializers import UserSerializer, AllContactInfoSerializer


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = serializers.CharField(default='customer')
    username = serializers.SerializerMethodField('customer_username')
    contact_info = serializers.SerializerMethodField('get_contact_info')

    def get_contact_info(self, obj):
        return AllContactInfoSerializer(obj.user.contactInfo).data

    def customer_username(self, obj):
        return obj.user.username[:obj.user.username.find('@')]

    class Meta:
        model = models.Customer
        fields = ['id', 'username', 'user', 'contact_info', 'role']
