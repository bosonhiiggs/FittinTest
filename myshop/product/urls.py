from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    # ProductViewSet,
    # CategoryViewSet,
    ProductListView,
    ProductDetailView,
    CategoryListView,
)

router = DefaultRouter()
# router.register(r'products', ProductViewSet)
# router.register(r'categories', CategoryViewSet)

app_name = 'product'

urlpatterns = [
    # path('', include(router.urls)),

    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='product-detail'),

    path('categories/', CategoryListView.as_view(), name='category-list'),
]
