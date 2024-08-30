from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from cart.models import Cart, CartItem
from order.models import Order, OrderItem
from product.models import Product, Category

client = APIClient()


class OrderTests(APITestCase):
    def setUp(self):
        self.client = client
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
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

        self.order_url = reverse('order:order-list')

    def test_create_order(self):
        response = self.client.post(self.order_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        order = Order.objects.first()
        self.assertEqual(order.total_price, 200.00)  # 100 * 2 = 200
        self.assertEqual(order.user, self.user)

        self.assertFalse(self.cart.items.exists())