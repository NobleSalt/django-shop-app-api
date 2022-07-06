from django.contrib import admin

from api.models import Cart, CartItem, Category, Product, Store, SubCategory

# Register your models here.
admin.site.register(
    [
        Store,
        Category,
        SubCategory,
        Product,
        Cart,
        CartItem,
    ]
)
