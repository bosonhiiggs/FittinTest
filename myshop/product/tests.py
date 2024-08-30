from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from product.models import Category, Product


client = APIClient()


class CategoryTestCase(TestCase):
    def setUp(self):
        self.client = client
        self.parent_category = Category.objects.create(name='Test Category')
        self.sub_category = Category.objects.create(name='Test Subcategory', parent=self.parent_category)
        self.sub_category_second = Category.objects.create(name='Test Subcategory second', parent=self.parent_category)

        self.url_category_list = reverse('product:category-list')

    def test_category_list(self):
        response = self.client.get(self.url_category_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['subcategories'][0]['name'], self.sub_category.name)
        self.assertEqual(response.data[0]['subcategories'][1]['name'], self.sub_category_second.name)
        self.assertIsNotNone(response.data[0]['subcategories'])


class ProductTestCase(TestCase):

    def setUp(self):
        self.category = Category.objects.create(name="Категория", parent=None)
        self.product = Product.objects.create(
            name="Продукт",
            description="Описание продукта",
            image="http://example.com/image.jpg",
            price=1000,
            category=self.category,
            characteristics={"состав": "100% полиэстер"},
        )

        self.url_products_list = reverse('product:product-list')
        self.url_product_detail = reverse('product:product-detail', kwargs={'pk': self.product.id})

    def test_product_list(self):
        response = self.client.get(self.url_products_list)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], self.product.name)
        self.assertEqual(response.data[0]['category']['name'], self.category.name)

    def test_product_detail(self):
        response = self.client.get(self.url_product_detail)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], self.product.name)
        self.assertEqual(response.data['category']['name'], self.category.name)
        self.assertEqual(response.data['price'], "1000.00")

