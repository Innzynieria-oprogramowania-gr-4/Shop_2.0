from django.contrib import admin

from .models import Coupon

# kupon zarejestrowany w witrynie administracyjnej
admin.site.register(Coupon)