from .. import models
from rest_framework import serializers
from . import FeeSerializer
from django.shortcuts import get_object_or_404


class ProductImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductImage
        fields = [
            'id',
            'img'
        ]


class ProductSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    price_plan = serializers.SerializerMethodField('priceplan')
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True, required=False)
    images = ProductImgSerializer(many=True, required=False)

    def priceplan(self, obj):
        return FeeSerializer(
            sorted(obj.fees.all(), key=lambda x: x.duration()),
            many=True).data

    class Meta:
        model = models.Product
        fields = [
            'id',
            'title',
            'description',
            'company',
            'price_plan',
            'needed_deposit',
            'num_of_ratings',
            'avg_ratings',
            'is_available',
            'category',
            'sub_category',
            'tags',
            'images'
        ]


class ProductforOwnerSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()
    price_plan = serializers.SerializerMethodField('priceplan')
    category = serializers.SlugRelatedField(slug_field='name', queryset=models.Category.objects.all(), required=False)
    sub_category = serializers.SlugRelatedField(slug_field='name', queryset=models.SubCategory.objects.all(), required=False)
    tags = serializers.SlugRelatedField(slug_field='name', read_only=True, many=True, required=False)
    images = ProductImgSerializer(many=True, required=False)

    def priceplan(self, obj):
        return FeeSerializer(
            sorted(obj.fees.all(), key=lambda x: x.duration()),
            many=True).data

    # def create(self, validated_data):
    #     category_data = validated_data.pop('category', None)
    #     subcategory_data = validated_data.pop('sub_category', None)
    #     tags_data = validated_data.pop('tags', None)
    #     category = get_object_or_404(models.Category, name=category_data) if category_data is not None else None
    #     subcategory = get_object_or_404(models.SubCategory, name=subcategory_data) if category_data is not None else None
    #     tags = []
    #     for tag_data in tags_data:
    #         try:
    #             tag = models.Tag.objects.get(name=tag_data)
    #             tags.append(tag)
    #         except Exception:
    #             tag = models.Tag.objects.create(name=tag_data)
    #             tags.append(tag)
    #     product = models.Product.objects.create(**validated_data)
    #     product.category = category
    #     product.sub_category = subcategory
    #     for tag in tags:
    #         product.tags.add(tag)
    #     product.save()
    #     return product

    class Meta:
        model = models.Product
        fields = [
            'id',
            'title',
            'description',
            'company',
            'quantity',
            'num_of_ratings',
            'avg_ratings',
            'is_available',
            'price_plan',
            'needed_deposit',
            'num_of_ratings',
            'avg_ratings',
            'is_available',
            'category',
            'sub_category',
            'tags',
            'images'
        ]
