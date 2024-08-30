# order/views.py
from urllib import request

from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from order.common import send_order_email
from order.models import Order, OrderItem
from order.serializer import OrderSerializer


@extend_schema(
    summary='Create a new order',
    examples=[
        OpenApiExample(
            name='Post request order example',
            value={},
        )
    ]
)
class OrderListView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.get(user=user)

        if not cart.items.exists():
            return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        total_sum = sum(item.quantity * item.product.price for item in cart.items.all())

        order = Order.objects.create(user=user, total_price=total_sum)

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price
            )

        cart.items.all().delete()

        serializer = self.get_serializer(order)
        if user.email:
            send_order_email(user.email, total_sum=total_sum)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



