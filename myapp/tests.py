from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Order, Product


class StorefrontTests(TestCase):
	def setUp(self):
		self.product = Product.objects.create(
			name="Everyday Cup",
			slug="everyday-cup-test",
			category="Dining",
			description="A cup for your morning ritual.",
			price=Decimal("24.00"),
			image_url="https://example.com/cup.jpg",
			image_alt="A handmade ceramic cup",
		)

	def test_homepage_renders_searchable_catalog(self):
		response = self.client.get(reverse("home"), {"q": "morning"})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Everyday Cup")

	def test_cart_and_checkout_create_order_with_delivery(self):
		self.client.post(reverse("add_to_cart", args=[self.product.slug]))
		cart_response = self.client.get(reverse("cart"))

		self.assertContains(cart_response, "$32.00")
		response = self.client.post(
			reverse("checkout"),
			{
				"customer_name": "Sam Example",
				"email": "sam@example.com",
				"delivery_address": "10 Main Street, Example City",
			},
		)

		order = Order.objects.get()
		self.assertRedirects(response, reverse("order_success", args=[order.number]))
		self.assertEqual(order.total, Decimal("32.00"))
		self.assertEqual(order.items[0]["quantity"], 1)
		self.assertContains(self.client.get(reverse("cart")), "Your bag is taking a breather.")

	def test_empty_bag_cannot_open_checkout(self):
		response = self.client.get(reverse("checkout"))

		self.assertRedirects(response, reverse("home"))
		self.assertEqual(Order.objects.count(), 0)
