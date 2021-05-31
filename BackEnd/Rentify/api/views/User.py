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


# class CRUDCompany(viewsets.ModelViewSet):
#     queryset = models.Company.objects.all()
#     serializer_class = serializers.CompanySerializer
#
#     def get_permissions(self):
#         if self.request.method == 'POST':
#             return [permissions.AllowAny()]
#         else:
#             return [permissions.IsAuthenticated(), utilities.IsCompanyPermission(), utilities.IsOwnerCompany()]
#
#     def get_object(self):
#         return self.request.user.company
#
#
# class CRUDCustomer(viewsets.ModelViewSet):
#     queryset = models.Customer.objects.all()
#     serializer_class = serializers.CustomerSerializer
#
#     def get_permissions(self):
#         if self.request.method == 'POST':
#             return [permissions.AllowAny()]
#         else:
#             return [permissions.IsAuthenticated(), utilities.IsCustomerPermission(), utilities.IsOwnerCustomer()]
class GetUser(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        if hasattr(user, 'company'):
            company = serializers.CompanySerializer(user.company, context={'request': request})
            return Response(company.data, status.HTTP_200_OK)
        else:
            customer = serializers.CustomerSerializer(user.customer)
            return Response(customer.data, status.HTTP_200_OK)


class CreateUser(GenericAPIView):
    @csrf_exempt
    def post(self, request):
        data = request.data
        if not utilities.check_inputs(
                request,
                ['username', 'password', 'email', 'role', 'first_name', 'last_name']
        ):
            return Response({'massage': 'arguments error!'}, status.HTTP_400_BAD_REQUEST)
        if data['role'] == "company":
            try:
                new_user = User.objects.create_user(
                    username=data['email'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['last_name'])
                Token.objects.create(user=new_user)
            except Exception as e:
                print(e)
                return Response({'massage': str(e)}, status.HTTP_400_BAD_REQUEST)
            try:
                new_company = models.Company.objects.create(title=data['username'], user=new_user)
                if 'description' in data:
                    new_company.description = data['description']
                if 'open_from' in data:
                    new_company.open_from = data['open_from']
                if 'close_at' in data:
                    new_company.close_at = data['close_at']
                new_company.save()
                models.ContactInfo.objects.create(user=new_user)
            except Exception as e:
                print(e)
                return Response({'massage': str(e)}, status.HTTP_400_BAD_REQUEST)
            company = serializers.CompanySerializer(new_company)
            return Response(company.data, status.HTTP_201_CREATED)
        elif data['role'] == "customer":
            try:
                new_user = User.objects.create_user(
                    username=data['email'],
                    email=data['email'],
                    password=data['password'],
                    first_name=data['first_name'],
                    last_name=data['password'])
                Token.objects.create(user=new_user)
            except Exception as e:
                print(e)
                return Response({'massage': str(e)}, status.HTTP_400_BAD_REQUEST)
            try:
                new_customer = models.Customer.objects.create(user=new_user)
                models.ContactInfo.objects.create(user=new_user)
                models.Basket.objects.create(customer=new_customer)
            except Exception as e:
                print(e)
                return Response({'massage': str(e)}, status.HTTP_400_BAD_REQUEST)
            customer = serializers.CustomerSerializer(new_customer)
            return Response(customer.data, status.HTTP_201_CREATED)
        else:
            return Response({"role": "role is not specified!"}, status.HTTP_400_BAD_REQUEST)


class UpdateUser(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    @csrf_exempt
    def put(self, request):
        data = request.data
        if not utilities.check_inputs(request, ['username', 'first_name', 'last_name', 'password', 'email']):
            return Response({'massage': 'arguments error!'}, status.HTTP_400_BAD_REQUEST)
        user = request.user
        if hasattr(user, 'customer'):
            customer = user.customer
            user.email = data['email']
            user.username = data['email']
            user.set_password(data['password'])
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            customer.name = data['username']
            try:
                user.save()
                customer.save()
                customer = serializers.CustomerSerializer(customer)
                return Response(customer.data, status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'massage': str(e)}, status.HTTP_400_BAD_REQUEST)

        elif hasattr(user, 'company'):
            company = user.company
            user.email = data['email']
            user.username = data['email']
            user.set_password(data['password'])
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            company.title = data['username']
            if 'description' in data:
                company.description = data['description']
            if 'open_from' in data:
                company.open_from = data['open_from']
            if 'close_at' in data:
                company.close_at = data['close_at']
            try:
                user.save()
                company.save()
                company = serializers.CompanySerializer(company, context={'request': request})
                return Response(company.data, status.HTTP_200_OK)
            except Exception as e:
                print(e)
                return Response({'massage': str(e)}, status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"role": "role is not specified!"}, status.HTTP_400_BAD_REQUEST)


class CRUDAddress(viewsets.ModelViewSet):
    queryset = models.Address.objects.all()
    serializer_class = serializers.AddressSerializer
    permission_classes = [permissions.IsAuthenticated, utilities.IsCompanyPermission, utilities.IsOwnerOfContactInfoPermission]

    def perform_create(self, serializer):
        serializer.save(contactInfo=self.request.user.contactInfo)


class CRUDPhone(viewsets.ModelViewSet):
    queryset = models.PhoneNumber.objects.all()
    serializer_class = serializers.PhoneSerializer
    permission_classes = [permissions.IsAuthenticated, utilities.IsCompanyPermission, utilities.IsOwnerOfContactInfoPermission]

    def perform_create(self, serializer):
        serializer.save(contactInfo=self.request.user.contactInfo)


class CRUDCompanyImg(viewsets.ModelViewSet):
    queryset = models.CompanyImage.objects.all()
    serializer_class = serializers.CompanyImgSerializer
    permission_classes = [permissions.IsAuthenticated, utilities.IsCompanyPermission, utilities.IsOwnerPermissionCompany]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)


class CRUDSubscription(viewsets.ModelViewSet):
    queryset = models.CompanySubscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, utilities.IsCompanyPermission, utilities.IsOwnerPermissionCompany]

    def perform_create(self, serializer):
        serializer.save(company=self.request.user.company)
