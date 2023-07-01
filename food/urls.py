"""food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from foodApp.views import index, search, details, user_login, register_customer, logout_view, handle_form_submission, \
    cart, place_order, confirmed, filter_foods, remove_from_cart, edit_food, add_food, delete_food, contact

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', index),
                  path('search/', search, name='search_foods'),
                  path('contact/', contact, name="contact"),
                  path('foods/<int:food_id>/', details, name='food_details'),
                  path('login/', user_login),
                  path('register/', register_customer),
                  path('logout/', logout_view, name='logout'),
                  path('cart/', cart, name='cart'),
                  path('deliveryinfo/', place_order, name='confirm_delivery'),
                  path('confirmed/', confirmed, name='order_confirmed'),
                  path('filter/', filter_foods, name='filter_foods'),
                  path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
                  path('food/edit/<int:food_id>/', edit_food, name='food-edit'),
                  path('add/<int:food_id>/', handle_form_submission, name='add'),
                  path('add-food/', add_food, name='add_food'),
                  path('delete-food/<int:food_id>/', delete_food, name='delete_food'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
