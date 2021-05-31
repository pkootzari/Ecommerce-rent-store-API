# class CartActions(GenericAPIView):
#     queryset = models.Cart.objects.all()
#     serializer_class = serializers.CartSerializer
#     permission_classes = [utilities.IsCustomerPermission]
#
#     @csrf_exempt
#     def post(self, request):
#         # self.check_permissions(request)
#         try:
#             cart = models.Cart.objects.get(customer=request.user.customer)
#         except models.Cart.DoesNotExist:
#             invoice = models.Invoice.objects.create()
#             cart = models.Cart.objects.create(customer=request.user.customer, invoice=invoice)
#         for p in request.data['products'].split() if 'products' in request.data else []:
#             cart.products.add(get_object_or_404(models.Product, pk=int(p)))
#         cart.save()
#         serializer = serializers.CartSerializer(cart)
#         return Response(serializer.data, status.HTTP_200_OK)
#
#     def delete(self, request):
#         # self.check_permissions(request)
#         try:
#             cart = models.Cart.objects.get(customer=request.user.customer)
#             cart.delete()
#         except models.Cart.DoesNotExist:
#             return Response({'massage': 'No cart available!'}, status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#     def get(self, request):
#         # self.check_permissions(request)
#         try:
#             cart = models.Cart.objects.get(customer=request.user.customer)
#         except models.Cart.DoesNotExist:
#             return Response({'massage': 'No cart available!'}, status.HTTP_400_BAD_REQUEST)
#         serializer = serializers.CartSerializer(cart)
#         return Response(serializer.data, status.HTTP_200_OK)


# class DeleteFromCart(GenericAPIView):
#     queryset = models.Cart.objects.all()
#     serializer_class = serializers.CartSerializer
#     permission_classes = [utilities.IsCustomerPermission]
#
#     @csrf_exempt
#     def post(self, request):
#         # self.check_permissions(request)
#         if not utilities.check_inputs(request, ['products']):
#             return Response({'massage': 'arguments error!'}, status.HTTP_400_BAD_REQUEST)
#         try:
#             cart = models.Cart.objects.get(customer=request.user.customer)
#             for p in request.data['products'].split():
#                 product = models.Product.objects.get(pk=int(p))
#                 cart.products.remove(product)
#             cart.save()
#         except models.Cart.DoesNotExist:
#             return Response({'massage': 'No cart available!'}, status.HTTP_400_BAD_REQUEST)
#         except models.Product.DoesNotExist:
#             return Response({'massage': 'Product not found!'}, status.HTTP_400_BAD_REQUEST)
#         serializer = serializers.CartSerializer(cart)
#         return Response(serializer.data, status.HTTP_200_OK)


# class InvoiceDetail(GenericAPIView):
#     queryset = models.Invoice
#     serializer_class = serializers.InvoiceDetailSerializer
#     permission_classes = [utilities.IsCustomerPermission]
#
#     def get(self, request):
#         # self.check_permissions(request)
#         try:
#             cart = models.Cart.objects.get(customer=request.user.customer)
#             serializer = serializers.InvoiceDetailSerializer(cart.invoice)
#             return Response(serializer.data, status.HTTP_200_OK)
#         except models.Cart.DoesNotExist:
#             return Response({'massage': 'No cart available!'}, status.HTTP_400_BAD_REQUEST)
