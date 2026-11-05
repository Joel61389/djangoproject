from django.urls import path

from myapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("bag/", views.cart, name="cart"),
    path("bag/add/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/<uuid:number>/", views.order_success, name="order_success"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
]