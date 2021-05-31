from .. import models
from rest_framework import serializers


class PhoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PhoneNumber
        fields = ['id', 'title', 'number', 'display']
        extra_kwargs = {
            'title': {'required': True},
            'number': {'required': True}
        }


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Address
        fields = ['id', 'title', 'address', 'display']
        extra_kwargs = {
            'title': {'required': True},
            'number': {'required': True}
        }


class DisplayableContactInfoSerializer(serializers.ModelSerializer):
    phones = serializers.SerializerMethodField('get_phones')
    addresses = serializers.SerializerMethodField('get_addresses')

    def get_phones(self, obj):
        return PhoneSerializer(obj.phoneNumbers.filter(display=True), many=True).data

    def get_addresses(self, obj):
        return AddressSerializer(obj.addresses.filter(display=True), many=True).data

    class Meta:
        model = models.ContactInfo
        fields = ['id', 'phones', 'addresses']


class AllContactInfoSerializer(serializers.ModelSerializer):
    phones = serializers.SerializerMethodField('get_phones')
    addresses = serializers.SerializerMethodField('get_addresses')

    def get_phones(self, obj):
        return PhoneSerializer(obj.phoneNumbers.all(), many=True).data

    def get_addresses(self, obj):
        return AddressSerializer(obj.addresses.all(), many=True).data

    class Meta:
        model = models.ContactInfo
        fields = ['id', 'phones', 'addresses']
