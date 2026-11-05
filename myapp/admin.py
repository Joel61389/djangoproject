from django.contrib import admin

from .models import Order, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ("name", "category", "price", "is_active", "sort_order")
	list_filter = ("category", "is_active")
	search_fields = ("name", "description")
	prepopulated_fields = {"slug": ("name",)}


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ("number", "customer_name", "email", "total", "status", "created_at")
	list_filter = ("status", "created_at")
	search_fields = ("customer_name", "email", "number")
	readonly_fields = ("number", "items", "created_at")
