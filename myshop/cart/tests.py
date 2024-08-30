from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from cart.models import CartItem, Cart
from product.models import Product, Category


class CartTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
        )

        url_jwt = reverse('myauth:token-login')
        response = self.client.post(url_jwt, {'username': 'testuser', 'password': 'testpassword'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.category = Category.objects.create(
            name='Категория'
        )

        self.product = Product.objects.create(
            name='Продукт',
            description='Описание продукта',
            image='product/path/to/file.jpeg',
            price=100.0,
            category=self.category,
            characteristics={},
        )

        self.cart = Cart.objects.create(user=self.user)

        self.url_cart = reverse('cart:cart-detail')

    def test_cart(self):
        response = self.client.get(self.url_cart)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('id', response.data)
        self.assertIn('user', response.data)
        self.assertIn('items', response.data)

    def test_cart_to_add(self):
        data = {'product': self.product.id, 'quantity': 2}
        response = self.client.post(self.url_cart, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['total_price'], '200.00')

    def test_update_cart_item(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        response = self.client.put(self.url_cart, {'product': self.product.id, 'quantity': 3}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 3)
        self.assertEqual(response.data['total_price'], '300.00')

    def test_remove_from_cart(self):
        cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        response = self.client.delete(self.url_cart, {'product': self.product.id}, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

