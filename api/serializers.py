import json
from rest_framework import serializers
from django.contrib.auth import get_user_model

from api.models import Cart, CartItem, Category, Order, Product, Store, SubCategory

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]


class ProductSerializer(serializers.ModelSerializer):
    image_url = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["id", "date_created", "status", "cart_id","total"]


class CartItemSerializer(serializers.ModelSerializer):
    _product = serializers.SerializerMethodField("get_product")

    def get_product(self, obj):
        return ProductSerializer(instance=obj.product, read_only=True).data

    class Meta:
        model = CartItem
        fields = ["_product", "amount"]


class CartSerializer(serializers.ModelSerializer):
    cart_items = serializers.SerializerMethodField("getcart_items")

    def getcart_items(self, obj):
        return CartItemSerializer(
            instance=obj.cartitems.all(), read_only=True, many=True
        ).data

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "order_complete",
            "date_created",
            "date_updated",
            "cart_items",
        ]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SubCategorySerializer(serializers.ModelSerializer):
    category__name = serializers.SerializerMethodField("get_category_name")

    def get_category_name(self, obj):
        return obj.category.name

    class Meta:
        model = SubCategory
        fields = [
            "id",
            "name",
            "category__name",
        ]


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(read_only=True, many=True)
    image_url = serializers.SerializerMethodField("get_image_url")

    def get_image_url(self, obj):
        if obj.image:
            return f"http://localhost:8000{obj.image.url}"

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "image",
            "image_url",
            "sub_categories",
            "date_created",
            "date_updated",
        ]
