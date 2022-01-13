from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view()),
    path('shop-cakes/<int:shop_id>', views.ShopCakes.as_view()),
    path('about', views.AboutView.as_view()),
    path('products', views.ProductView.as_view()),
    path('cart', views.CartView.as_view()),
    path('cart/add/<int:cake_id>', views.CartAddView.as_view()),
    path('remove-item/<int:cart_id>', views.RemoveCartView.as_view()),
    path('cart/update', views.CartUpdateView.as_view()),
    path('checkout', views.CheckoutView.as_view()),
    path('place-order', views.PlaceOrderView.as_view()),
]
