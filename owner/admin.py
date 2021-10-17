from django.contrib import admin

# Register your models here.

from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from owner.models import Product,MyUser,Order,OrderItems
# Register your models here.


admin.site.register(Product)
admin.site.register(MyUser)

admin.site.register(Order)
admin.site.register(OrderItems)

