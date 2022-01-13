
from django.contrib import admin
from django.urls import path


from . import views

urlpatterns = [
    path('login', views.Login.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('registration', views.RegistrationView.as_view()),
    path('dashboard', views.Dashboard.as_view()),
    path('my-shops', views.MyShopView.as_view()),
    path('add-shop', views.AddShopView.as_view()),
    path('delete-shop/<int:shop_id>', views.DeleteShopView.as_view()),
    path('edit-shop/<int:shop_id>', views.EditShopView.as_view()),
    path('cakes', views.CakeView.as_view()),
    path('booking', views.BookingView.as_view()),
    path('add-cake', views.AddCakeView.as_view()),
    path('edit-cake/<int:edit_id>', views.EditCakeView.as_view()),
    path('add-flavour', views.AddFlavourView.as_view()),
    path('add-image', views.AddImageView.as_view()),
    path('delete-cake/<int:cake_id>', views.DeleteCakeView.as_view()),
    path('cake-details/<int:cake_id>', views.CakeDetailsView.as_view()),

]
