from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class UserRole(models.Model):
    name = models.CharField(max_length=32)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'user_role'


class User(AbstractUser):
    username = models.CharField(max_length=12, unique=False, null=True)
    email = models.EmailField(max_length=128, unique=True)
    phone = models.CharField(max_length=15, unique=True)
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, null=True)
    address1 = models.CharField(max_length=32, null=True)
    address2 = models.CharField(max_length=32, null=True)
    city = models.CharField(max_length=32, null=True)
    pincode = models.PositiveIntegerField(null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    class Meta:
        db_table = 'user'

class Shop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    address = models.TextField()
    location = models.CharField(max_length=16)
    pincode = models.IntegerField()
    image = models.ImageField(upload_to='media/shops/', null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'shops'

class Category(models.Model):
    name = models.CharField(max_length=32)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'category'

class CakeWeight(models.Model):
    name = models.CharField(max_length=12)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'cake_weight'

class Cake(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    weight = models.ForeignKey(CakeWeight, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    cake_image = models.ImageField(upload_to='media/CakeImages/', null=True)
    flavour = models.CharField(max_length=32, null=True)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'cake'

class CakeFlavour(models.Model):
    name = models.CharField(max_length=32)
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'cake_flavour'

class CakeImage(models.Model):
    image = models.ImageField(upload_to='media/CakeImages/')
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'cake_images'

class Booking(models.Model):
    cake = models.ForeignKey(Cake, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    total_price = models.FloatField()
    create_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'booking'