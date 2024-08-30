from django.shortcuts import render
from django.http import HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.generics import RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer


# class CartView(RetrieveAPIView):
#     serializer_class = CartSerializer
#     permission_classes = [IsAuthenticated]
#
#     def get_object(self):
#         cart, created = Cart.objects.get_or_create(user=self.request.user)
#         result = {
#             "cart": cart,
#             "created": created
#         }
#         return result
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()['cart']
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#
# class AddToCartView(CreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartItemSerializer
#
#     def get_object(self):
#         cart, created = Cart.objects.get_or_create(user=self.request.user)
#         result = {
#             "cart": cart,
#             "created": created
#         }
#         return result
#
#     def post(self, request, *args, **kwargs):
#         cart = self.get_object()['cart']
#         product = request.data['product']
#         quantity = int(request.data.get('quantity', 1))
#
#         cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product)
#         if not created:
#             cart_item.quantity += quantity
#         else:
#             cart_item.quantity = quantity
#
#         cart_item.save()
#         serializer = CartSerializer(cart_item)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#
# class UpdateCartItemView(UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartItemSerializer
#     queryset = CartItem.objects.all()
#
#     def get_object(self):
#         cart_item = super().get_object()
#         if cart_item.cart.user != self.request.user:
#             self.permission_denied(self.request)
#         return cart_item
#
#     def update(self, request, *args, **kwargs):
#         partial = kwargs.pop('partial', False)
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=partial)
#         serializer.is_valid(raise_exception=True)
#         self.perform_update(serializer)
#         return Response(serializer.data)
#
#
# class RemoveFromCartView(DestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CartItemSerializer
#     queryset = CartItem.objects.all()
#
#     def get_object(self):
#         cart_item = super().get_object()
#         if cart_item.cart.user != self.request.user:
#             self.permission_denied(self.request)
#         return cart_item
#
#     def delete(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary='Get cart details',
        responses={
            200: CartSerializer,
            404: 'Cart not found'
        }
    )
    def get_cart(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart

    def get(self, request, *args, **kwargs):
        cart = self.get_cart()
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Post to add product',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'product': {
                        'type': 'string',
                        'description': 'ID of the product to add'
                    },
                    'quantity': {
                        'type': 'integer',
                        'description': 'Quantity of the product'
                    }
                },
                'example': {
                    'product': 'product_id',
                    'quantity': 2
                }
            }
        },
        responses={
            201: CartSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        cart = self.get_cart()
        product = request.data['product']
        quantity = int(request.data.get('quantity', 1))

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product_id=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        summary='Put to add product',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'product': {
                        'type': 'string',
                        'description': 'ID of the product to add'
                    },
                    'quantity': {
                        'type': 'integer',
                        'description': 'Quantity of the product'
                    }
                },
                'example': {
                    'product': 'product_id',
                    'quantity': 2
                }
            }
        },
        responses={
            201: CartSerializer,
            400: 'Bad Request'
        }
    )
    def put(self, request, *args, **kwargs):
        cart = self.get_cart()
        product = request.data['product']
        quantity = int(request.data.get('quantity', 1))

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product)
        except CartItem.DoesNotExist:
            return Response({"error": "Товар не найден в корзине"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.quantity = quantity
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        summary='Delete product from cart',
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'product': {
                        'type': 'string',
                        'description': 'ID of the product to remove'
                    }
                },
                'example': {
                    'product': 'product_id'
                }
            }
        },
        responses={
            204: 'No Content',
            404: 'Product not found in cart'
        }
    )
    def delete(self, request, *args, **kwargs):
        cart = self.get_cart()
        product = request.data['product']

        try:
            cart_item = CartItem.objects.get(cart=cart, product_id=product)
        except CartItem.DoesNotExist:
            return Response({"error": "Товар не найден в корзине"}, status=status.HTTP_404_NOT_FOUND)

        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
