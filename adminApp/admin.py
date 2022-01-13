from django.contrib import admin

# Register your models here.
from adminApp.models import *

admin.site.register(UserRole)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Cake)
admin.site.register(CakeFlavour)
admin.site.register(CakeImage)
admin.site.register(Booking)
