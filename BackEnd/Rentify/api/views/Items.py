from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions
from .. import serializers
from django.contrib.auth.models import User
from rest_framework.decorators import action
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from .. import utilities
from .. import models


class CRUDItem(viewsets.ModelViewSet):
    serializer_class = serializers.ItemSerializer
    permission_classes = [permissions.IsAuthenticated, utilities.IsCustomerPermission, utilities.IsOwnerPermissionCustomer]

    def get_queryset(self):
        return models.Item.objects.filter(customer=self.request.user.customer).exclude(status=models.Item.STATUS_CHOICES[0][0])

    def perform_create(self, serializer):
        return serializer.save(customer=self.request.user.customer)

    # def create(self, request, *args, **kwargs):
    #     try:
    #         super().create(request, *args, **kwargs)
    #     except


class CRUDBasket(viewsets.ModelViewSet):
    serializer_class = serializers.ItemSerializer
    permission_classes = [permissions.IsAuthenticated, utilities.IsCustomerPermission, utilities.IsOwnerPermissionCustomer]

    def get_queryset(self):
        return models.Item.objects.filter(customer=self.request.user.customer, status=models.Item.STATUS_CHOICES[0][0])
