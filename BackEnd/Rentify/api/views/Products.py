from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework import permissions
from .. import serializers
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from .. import utilities
from .. import models


class ProductCRUD(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    # permission_classes = [permissions.IsAuthenticated, utilities.IsCompanyPermission, utilities.IsOwnerPermission]
    serializer_class = serializers.ProductSerializer

    def add_tags_to_instance(self, instance, tags):
        instance.tags.clear()
        for tag in tags.split():
            t, _ = models.Tag.objects.get_or_create(name=tag)
            instance.tags.add(t)
        instance.save()
        return instance

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        model_instance = self.perform_create(serializer)
        tag_data = request.data['tags'] if 'tags' in request.data else ""
        model_instance = self.add_tags_to_instance(model_instance, tag_data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializers.ProductforOwnerSerializer(model_instance).data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        model_instance = self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        tag_data = request.data['tags'] if 'tags' in request.data else ""
        model_instance = self.add_tags_to_instance(model_instance, tag_data)
        return Response(serializers.ProductforOwnerSerializer(model_instance).data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        return serializer.save(company=self.request.user.company)

    def perform_update(self, serializer):
        return serializer.save()

    def get_permissions(self):
        owner_permissions = [permissions.IsAuthenticated(), utilities.IsCompanyPermission(), utilities.IsOwnerPermissionCompany()]
        open_permissions = [permissions.AllowAny()]
        if self.action == 'rate':
            return [permissions.IsAuthenticated()]
        if self.request.method == 'GET':
            return open_permissions
        else:
            return owner_permissions

    def get_serializer_class(self):
        if self.action == 'list':
            return self.serializer_class
        if self.action == 'create':
            return serializers.ProductforOwnerSerializer
        if permissions.IsAuthenticated().has_permission(self.request, self) and \
                utilities.IsCompanyPermission().has_permission(self.request, self) and \
                utilities.IsOwnerPermissionCompany().has_object_permission(self.request, self, self.get_object()):
            return serializers.ProductforOwnerSerializer
        return self.serializer_class

    @action(methods=['get'], detail=False)
    def indexProduct(self, request):
        products = sorted(models.Product.objects.all(), key=lambda x: x.avg_ratings(), reverse=True)
        serializer = serializers.ProductSerializer(products, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def rate(self, request, pk):
        data = request.data
        rating_serializer = serializers.RatingsSerializer(data=request.data)
        rating_serializer.is_valid(raise_exception=True)
        product = self.get_object()
        user = request.user
        try:
            rating = models.Rating.objects.get(user=user, product=product)
            rating.stars = int(data['stars'])
            rating.save()
            serializer = serializers.RatingsSerializer(rating)
            return Response(serializer.data, status.HTTP_200_OK)
        except Exception:
            rating = models.Rating.objects.create(user=user, product=product, stars=int(data['stars']))
            serializer = serializers.RatingsSerializer(rating)
            return Response(serializer.data, status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def addFee(self, request, pk):
        data = request.data
        fee_serializer = serializers.FeeSerializer(data=data)
        fee_serializer.is_valid(raise_exception=True)
        product = self.get_object()
        try:
            fee = product.fees.get(time_unit=int(data['time_unit']), amount=int(data['amount']))
            fee.price = float(data['price'])
            fee.save()
            return Response(serializers.ProductforOwnerSerializer(product).data, status.HTTP_200_OK)
        except Exception:
            fee = models.Fee.objects.create(
                time_unit=int(data['time_unit']),
                amount=int(data['amount']),
                price=float(data['price']),
                product=product
            )
            return Response(serializers.ProductforOwnerSerializer(product).data, status.HTTP_200_OK)

    @action(methods=['delete'], detail=True)
    def deleteFee(self, request, pk):
        data = request.data
        product = self.get_object()
        if not utilities.check_inputs(request, ['fee_id']):
            return Response({'massage': 'argument error!'}, status.HTTP_400_BAD_REQUEST)
        try:
            fee_id = int(data['fee_id'])
            fee = get_object_or_404(models.Fee, pk=fee_id)
            if fee not in product.fees.all():
                return Response({'massage': "price plan doesn't belong to this product"}, status.HTTP_400_BAD_REQUEST)
            fee.delete()
            return Response(serializers.ProductforOwnerSerializer(product), status.HTTP_200_OK)
        except Exception as e:
            return Response({'massage': 'argument error!'}, status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def addImg(self, request, pk):
        data = request.data
        img_serializer = serializers.ProductImgSerializer(data=data)
        img_serializer.is_valid(raise_exception=True)
        product = self.get_object()
        img_serializer.save(product=product)
        return Response(serializers.ProductforOwnerSerializer(product).data, status.HTTP_200_OK)

    @action(methods=['delete'],detail=True)
    def deleteImg(self, request, pk):
        data = request.data
        product = self.get_object()
        if not utilities.check_inputs(request, ['img_id']):
            return Response({'massage': 'argument error!'}, status.HTTP_400_BAD_REQUEST)
        try:
            img_id = int(data['img_id'])
        except:
            return Response({'massage': 'argument error!'}, status.HTTP_400_BAD_REQUEST)
        img = get_object_or_404(models.ProductImage, pk=img_id)
        if img not in product.images.all():
            return Response({'massage': "image doesn't belong to this product"}, status.HTTP_400_BAD_REQUEST)
        img.delete()
        return Response(serializers.ProductforOwnerSerializer(product).data, status.HTTP_200_OK)
