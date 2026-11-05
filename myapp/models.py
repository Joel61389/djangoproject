import uuid

from django.db import models


class Product(models.Model):
	name = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	category = models.CharField(max_length=60)
	description = models.CharField(max_length=240)
	price = models.DecimalField(max_digits=8, decimal_places=2)
	image_url = models.URLField()
	image_alt = models.CharField(max_length=180)
	label = models.CharField(max_length=40, blank=True)
	is_active = models.BooleanField(default=True)
	sort_order = models.PositiveSmallIntegerField(default=0)

	class Meta:
		ordering = ["sort_order", "name"]

	def __str__(self):
		return self.name


class Order(models.Model):
	class Status(models.TextChoices):
		NEW = "new", "New"
		PROCESSING = "processing", "Processing"
		COMPLETE = "complete", "Complete"
		CANCELLED = "cancelled", "Cancelled"

	number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
	customer_name = models.CharField(max_length=120)
	email = models.EmailField()
	delivery_address = models.TextField(max_length=500)
	items = models.JSONField()
	total = models.DecimalField(max_digits=9, decimal_places=2)
	status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at"]

	def __str__(self):
		return f"Order {str(self.number)[:8]}"
