from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser, Food, RestaurantOwner, Category, Cart, DeliveryInfo, Order


# Register your models here.


class FoodAdmin(admin.ModelAdmin):
    pass


class RestaurantOwnerAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class CartAdmin(admin.ModelAdmin):
    pass



class DeliveryInfoAdmin(admin.ModelAdmin):
    pass


class OrderAdmin(admin.ModelAdmin):
    pass


class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('role',)


class CustomUserAdmin(UserAdmin):
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff',
        'role', )

    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ('Additional info', {
            'fields': ('role',)
        })
    )

    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('User Roles', {
            'fields': ('role',)
        })
    )
    add_form = CustomUserCreationForm


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(RestaurantOwner, RestaurantOwnerAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(DeliveryInfo, DeliveryInfoAdmin)
admin.site.register(Order, OrderAdmin)
