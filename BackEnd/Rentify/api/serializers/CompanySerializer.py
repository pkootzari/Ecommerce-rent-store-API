from .. import models
from rest_framework import serializers
from ..serializers import UserSerializer, AllContactInfoSerializer
from rest_framework.authtoken.models import Token


class CompanyImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanyImage
        fields = [
            'id',
            'img'
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CompanySubscription
        fields = [
            'id',
            'plan_title',
            'starts',
            'ends'
        ]


class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    images = CompanyImgSerializer(many=True)
    products = serializers.HyperlinkedRelatedField(view_name='product-detail', read_only=True, many=True)
    role = serializers.CharField(default='company')
    contact_info = serializers.SerializerMethodField('get_contact_info')

    def get_contact_info(self, obj):
        return AllContactInfoSerializer(obj.user.contactInfo).data

    class Meta:
        model = models.Company
        fields = [
            'id',
            'title',
            'description',
            'user',
            'role',
            'products',
            'images',
            'contact_info',
            'open_from',
            'close_at',
            'has_active_plan'
        ]
