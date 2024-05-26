from django.test import TestCase
from .models import Product, User
from django.urls import reverse


class ProductViewsCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123",
            email="test@example.com",
            first_name="Test",
            last_name="User",
            role="Administrator"
        )
        self.client.login(username="testuser", password="password123")

    def test_add_product(self):
        response = self.client.post(reverse('add_product'), {
            'product_name': 'New Product',
            'description': 'This is a new product',
            'category': 'New Category',
            'unit_price': 12.99,
            'reorder_level': 6
        })

        self.assertEqual(response.status_code, 302)

    def test_update_product(self):
        Product.objects.create(
            product_name="New Product",
            description="This is a new Product",
            category="New Category",
            unit_price=12.99,
            reorder_level=6
        )

        response = self.client.put(
            reverse('update_product', kwargs={'pk': 1}),
            {
                'product_name': 'Test Product',
                'description': 'Updated description',
                'category': 'Test Category',
                'unit_price': 12.99,
                'reorder_level': 5
            },
            content_type='application/json')

        self.assertEqual(response.status_code, 302)

        updated_product = Product.objects.get(pk=1)
        self.assertEqual(updated_product.description, 'This is a new Product')

    def test_search_product(self):
        product_name = 'Test Product'

        Product.objects.create(
            product_name=product_name,
            description="This is a new Product",
            category="New Category",
            unit_price=12.99,
            reorder_level=6
        )

        response = self.client.get(reverse('search_product'), {
                                   'query': product_name})
        self.assertEqual(response.status_code, 200)
        results = response.context['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].product_name, product_name)
