import uuid

from django.db import migrations, models


def add_starter_products(apps, schema_editor):
    Product = apps.get_model("myapp", "Product")
    products = [
        (
            "Arc Table Lamp", "arc-table-lamp", "Lighting",
            "A sculptural little glow for slow evenings and quiet corners.", "78.00",
            "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=900&q=85",
            "Warm ceramic table lamp glowing beside a book", "Bestseller", 1,
        ),
        (
            "Sunday Stoneware Set", "sunday-stoneware-set", "Dining",
            "Hand-finished stoneware for the everyday table, made to mix and match.", "64.00",
            "https://images.unsplash.com/photo-1490312278390-ab64016e0aa9?auto=format&fit=crop&w=900&q=85",
            "Neutral handmade ceramic plates and bowls", "Small batch", 2,
        ),
        (
            "Ripple Glass Pitcher", "ripple-glass-pitcher", "Dining",
            "A softly rippled glass pitcher that makes water feel like a ritual.", "42.00",
            "https://images.unsplash.com/photo-1514228742587-6b1558fcca3d?auto=format&fit=crop&w=900&q=85",
            "Clear textured glass pitcher on a dining table", "", 3,
        ),
        (
            "Cloud Cotton Throw", "cloud-cotton-throw", "Textiles",
            "A breathable, textured cotton layer for the sofa, bed, or anywhere.", "89.00",
            "https://images.unsplash.com/photo-1600210492486-724fe5c67fb0?auto=format&fit=crop&w=900&q=85",
            "Soft neutral cotton throw draped across a sofa", "Made with care", 4,
        ),
        (
            "Soft Form Vase", "soft-form-vase", "Objects",
            "A playful, tactile shape for fresh stems or a shelf all on its own.", "36.00",
            "https://images.unsplash.com/photo-1578500494198-246f612d3b3d?auto=format&fit=crop&w=900&q=85",
            "Sculptural handmade vase with a single leafy stem", "", 5,
        ),
        (
            "Gathering Tray", "gathering-tray", "Objects",
            "A solid wood catch-all for the daily essentials you reach for most.", "48.00",
            "https://images.unsplash.com/photo-1618221195710-dd6b41faaea6?auto=format&fit=crop&w=900&q=85",
            "Wooden serving tray styled with everyday objects", "Thoughtful pick", 6,
        ),
    ]
    for name, slug, category, description, price, image_url, image_alt, label, sort_order in products:
        Product.objects.create(
            name=name,
            slug=slug,
            category=category,
            description=description,
            price=price,
            image_url=image_url,
            image_alt=image_alt,
            label=label,
            sort_order=sort_order,
        )


def remove_starter_products(apps, schema_editor):
    Product = apps.get_model("myapp", "Product")
    Product.objects.filter(slug__in=[
        "arc-table-lamp", "sunday-stoneware-set", "ripple-glass-pitcher",
        "cloud-cotton-throw", "soft-form-vase", "gathering-tray",
    ]).delete()


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("number", models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ("customer_name", models.CharField(max_length=120)),
                ("email", models.EmailField(max_length=254)),
                ("delivery_address", models.TextField(max_length=500)),
                ("items", models.JSONField()),
                ("total", models.DecimalField(decimal_places=2, max_digits=9)),
                ("status", models.CharField(choices=[("new", "New"), ("processing", "Processing"), ("complete", "Complete"), ("cancelled", "Cancelled")], default="new", max_length=12)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("slug", models.SlugField(unique=True)),
                ("category", models.CharField(max_length=60)),
                ("description", models.CharField(max_length=240)),
                ("price", models.DecimalField(decimal_places=2, max_digits=8)),
                ("image_url", models.URLField()),
                ("image_alt", models.CharField(max_length=180)),
                ("label", models.CharField(blank=True, max_length=40)),
                ("is_active", models.BooleanField(default=True)),
                ("sort_order", models.PositiveSmallIntegerField(default=0)),
            ],
            options={"ordering": ["sort_order", "name"]},
        ),
        migrations.RunPython(add_starter_products, remove_starter_products),
    ]