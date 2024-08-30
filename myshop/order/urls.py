from django.urls import path

from order.views import OrderListView

app_name = 'order'

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
]
