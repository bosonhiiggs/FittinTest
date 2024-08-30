from django.contrib import admin

from .forms import ProductAdminForm
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ['id', 'name', 'description', 'price', 'category']
    search_fields = ['name', 'description']
    list_filter = ['category', 'price']
    ordering = ['id']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent']
    search_fields = ['name']
    list_filter = ['parent']
    ordering = ['id']
