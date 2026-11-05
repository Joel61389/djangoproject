from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import CheckoutForm
from .models import Order, Product


def cart_details(request):
    cart = request.session.get("cart", {})
    products = Product.objects.filter(is_active=True, slug__in=cart.keys())
    lines = []
    total = Decimal("0.00")
    for product in products:
        quantity = max(1, min(int(cart.get(product.slug, 1)), 99))
        line_total = product.price * quantity
        lines.append({"product": product, "quantity": quantity, "line_total": line_total})
        total += line_total
    return lines, total


def shared_context(request, **context):
    lines, total = cart_details(request)
    context.update({"cart_count": sum(line["quantity"] for line in lines), "cart_total": total})
    return context


def delivery_fee(subtotal):
    return Decimal("0.00") if subtotal >= Decimal("100.00") else Decimal("8.00")


def home(request):
    products = Product.objects.filter(is_active=True)
    query = request.GET.get("q", "").strip()
    category = request.GET.get("category", "")
    sort = request.GET.get("sort", "featured")
    if query:
        products = products.filter(name__icontains=query) | products.filter(description__icontains=query)
    if category:
        products = products.filter(category=category)
    if sort == "price-low":
        products = products.order_by("price", "name")
    elif sort == "price-high":
        products = products.order_by("-price", "name")
    elif sort == "name":
        products = products.order_by("name")
    categories = Product.objects.filter(is_active=True).values_list("category", flat=True).distinct()
    return render(
        request,
        "home.html",
        shared_context(
            request,
            products=products,
            categories=categories,
            query=query,
            selected_category=category,
            selected_sort=sort,
        ),
    )


def add_to_cart(request, slug):
    if request.method != "POST":
        return redirect("home")
    product = get_object_or_404(Product, slug=slug, is_active=True)
    cart = request.session.get("cart", {})
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1
    cart[product.slug] = min(99, max(1, int(cart.get(product.slug, 0)) + quantity))
    request.session["cart"] = cart
    messages.success(request, f"{product.name} added to your bag.")
    referer = request.META.get("HTTP_REFERER", "")
    if url_has_allowed_host_and_scheme(referer, allowed_hosts={request.get_host()}):
        return redirect(referer)
    return redirect("home")


def cart(request):
    if request.method == "POST":
        cart_data = request.session.get("cart", {})
        action = request.POST.get("action")
        slug = request.POST.get("slug", "")
        if action == "remove":
            cart_data.pop(slug, None)
            messages.info(request, "Item removed from your bag.")
        elif action == "update" and slug in cart_data:
            try:
                quantity = int(request.POST.get("quantity", 1))
            except (TypeError, ValueError):
                quantity = 1
            cart_data[slug] = min(99, max(1, quantity))
            messages.success(request, "Your bag has been updated.")
        request.session["cart"] = cart_data
        return redirect("cart")
    lines, total = cart_details(request)
    fee = delivery_fee(total)
    return render(
        request,
        "cart.html",
        shared_context(request, lines=lines, total=total, delivery_fee=fee, grand_total=total + fee),
    )


def checkout(request):
    lines, total = cart_details(request)
    if not lines:
        messages.info(request, "Add something lovely to your bag before checking out.")
        return redirect("home")
    form = CheckoutForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        order = form.save(commit=False)
        order.items = [
            {
                "name": line["product"].name,
                "quantity": line["quantity"],
                "unit_price": str(line["product"].price),
                "line_total": str(line["line_total"]),
            }
            for line in lines
        ]
        order.total = total + delivery_fee(total)
        order.save()
        request.session["cart"] = {}
        return redirect("order_success", number=order.number)
    return render(
        request,
        "checkout.html",
        shared_context(
            request,
            form=form,
            lines=lines,
            total=total,
            delivery_fee=delivery_fee(total),
            grand_total=total + delivery_fee(total),
        ),
    )


def order_success(request, number):
    order = get_object_or_404(Order, number=number)
    return render(request, "order_success.html", shared_context(request, order=order))


def about(request):
    return render(request, "about.html", shared_context(request))


def contact(request):
    return render(request, "contacts.html", shared_context(request))