import json
from django.shortcuts import render
from .serializers import *
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.views.decorators.csrf import csrf_exempt
from django_filters import filters
from rest_framework.views import APIView

from django.db.models import Count, Q

# Create your views here.
def index(request):

    return Response(data={"msg": "success"})


@csrf_exempt
def create_user(request):

    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def get_login(request, email):

    try:
        user = User.objects.filter(email=email)
    except:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = UserSerializer(user, many=True)

        return Response(serializer.data, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
def get_user(request, id):

    try:
        user = User.objects.get(id=id)
    except:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = UserSerializer(user, many=True)

        return Response(serializer.data, safe=False, status=status.HTTP_200_OK)


class FetchCart(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, *args, **kwargs):
        # get user
        user = self.request.user
        # create cart
        cart, created = Cart.objects.get_or_create(user=user, order_complete="NO")
        # if created:
        #     # create cart item
        #     print(dir(cart.cartitems))
        # else:
        #     # cart.cartitems.get_or_create(product=product, quantity=1)
        #     print("hehe")
        # # get products
        # # for product in products:
        # #     print(product)
        # # prod_id = product["id"]
        # # prod_qty = product["quantity"]
        # # cartItem = CartItem()
        # # cartItem.cart = cart
        # # cartItem.quantity = prod_qty
        # # cartItem.product=Product.objects.get(id=prod_id)
        # # cartItem.save()
        # # create cart item
        # # add cart items to cart

        serializer = CartSerializer(cart, many=False)
        return Response(serializer.data)


class CartAction(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, *args, **kwargs):
        # get user
        user = self.request.user
        # get or create user cart
        cart, created = Cart.objects.get_or_create(user=user, order_complete="NO")
        # parse request body to dictionary
        data = JSONParser().parse(self.request)
        product_id = data["product_id"]
        product_amount = data["product_amount"]
        action = data["action"]
        # get product by id
        product = Product.objects.get(id=product_id)
        if created:
            cart.cartitems.get_or_create(product=product, amount=product_amount)
        else:
            if action == "remove":
                cartitem = cart.cartitems.get(product=product)
                print("cartitem", cartitem)
                cartitem.delete()
            else:
                cartitem, created_cartitem = cart.cartitems.get_or_create(
                    product=product
                )
                cartitem.amount = product_amount
                cartitem.save()

        serializer = CartSerializer(instance=cart)
        return Response(serializer.data)


@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes(permission_classes=[IsAuthenticatedOrReadOnly])
@authentication_classes(authentication_classes=[TokenAuthentication])
def product_list(request):

    if request.method == "GET":
        products = Product.objects.all().order_by("-date_created")
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data)

    if request.method == "POST":
        # data = JSONParser().parse(request)
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@csrf_exempt
@api_view(["GET", "POST"])
@permission_classes(permission_classes=[IsAuthenticatedOrReadOnly])
@authentication_classes(authentication_classes=[TokenAuthentication])
def category_list(request):

    if request.method == "GET":
        categories = Category.objects.all().order_by("-date_created")
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data)

    if request.method == "POST":
        # data = JSONParser().parse(request)
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


@csrf_exempt
def get_product_by_id(request, id):

    try:
        product = Product.objects.get(id=id)
    except:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data, safe=False, status=status.HTTP_200_OK)
    if request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "DELETE":
        product.delete()
        return Response(status=status.HTTP_201_CREATED)


@csrf_exempt
def product_seller(request, id):
    try:
        product = Product.objects.get(id=id)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data, safe=False)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


@csrf_exempt
def products_by_category(request, category):
    try:
        get_category = Category.objects.get(name=category)
        products = get_category.get_products_by_category
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ProductSerializer(data=products, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


@csrf_exempt
def cart_list(request, user_id):
    if request.method == "POST":
        try:
            get_cart_by_userid = Cart.objects.get(user_id=user_id)
            serializer = CartSerializer(get_cart_by_userid)
        except:
            return HttpResponse(serializer.errors, status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, safe=False, status=status.HTTP_200_OK)


@csrf_exempt
def create_store(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        serializer = StoreSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
def get_store(request, userId):
    if request.method == "GET":
        try:
            store = Store.objects.get(user__id=userId)
            serializer = StoreSerializer(store, many=False)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        return Response(serializer.data, safe=False, status=status.HTTP_200_OK)


class search_product(generics.ListAPIView):
    search_fields = (
        "store__name",
        "name",
        "description",
        "sub_category__name",
        "price",
        "thumbnail",
        "image",
        "stock",
        "condition",
        "rating",
    )
    filter_backends = filters.AllValuesFilter
    queryset = Product.objects.all()
    serializer_class = ProductSerializer()


def filter_min_price(request, min_price):
    if request.method == "GET":
        try:
            products = Product.objects.filter(price__gte=min_price)
            serializer = ProductSerializer(products, many=True)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


def filter_max_price(request, max_price):
    if request.method == "GET":
        try:
            products = Product.objects.filter(price__lte=max_price)
            serializer = ProductSerializer(products, many=True)
        except:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, safe=False, status=status.HTTP_200_OK)


def filter_rating(request, rating):

    try:
        products = Product.objects.filter(rating__gte=rating)
        serializer = ProductSerializer(products, many=True)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, safe=False, status=status.HTTP_200_OK)


def filter_condition(request, condition):

    try:
        products = Product.objects.filter(condition__gte=condition)
        serializer = ProductSerializer(products, many=True)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, safe=False, status=status.HTTP_200_OK)


def filter_price_and_condition(request, min_price, max_price, condition):

    try:
        products = Product.objects.filter(price_range(min_price, max_price)).filter(
            condition=condition
        )
        serializer = ProductSerializer(products, many=True)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, safe=False, status=status.HTTP_200_OK)


def filter_rating_and_condition(request, rating, condition):

    try:
        products = Product.objects.filter(rating_gte=rating).filter(condition=condition)
        serializer = ProductSerializer(products, many=True)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, safe=False, status=status.HTTP_200_OK)


def filter_all(request, min_price, max_price, rating, condition):

    try:
        products = (
            Product.objects.filter(price_range(min_price, max_price))
            .filter(rating_gte=rating)
            .filter(condition=condition)
        )
        serializer = ProductSerializer(products, many=True)
    except:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)
    return Response(serializer.data, safe=False, status=status.HTTP_200_OK)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, *args, **kwargs):
        # get user
        user = self.request.user
        # get or create user cart
        # cart, created = Cart.objects.get_or_create(user=user, order_complete="NO")
        # parse request body to dictionary
        data = JSONParser().parse(self.request)

        action = data["action"]
        """
        TODO feature: total_order
        TODO feature: pending_order
        TODO feature: processing_order
        TODO feature: complete_order
        """
        # get product by id
        response = {}
        order = Order.objects.filter(user=user)
        orders = OrderSerializer(order, many=True)
        if action == "dashboard":
            pending_order = Order.objects.filter(user=user, status="PENDING")
            processing_order = Order.objects.filter(user=user, status="PROCESSING")
            complete_order = Order.objects.filter(user=user, status="DELIVERED")
            canceled_order = Order.objects.filter(user=user, status="CANCELED")
            total_order = order.count()

            response = {
                "order": {
                    "pending_order": pending_order.count(),
                    "processing_order": processing_order.count(),
                    "complete_order": complete_order.count(),
                    "canceled_order": canceled_order.count(),
                    "total_order": total_order,
                },
                "orders": orders.data,
            }
        if action == "my_orders":
            order = Order.objects.filter(user=user)
            response = {"orders": orders.data, "order": {}}
        if action == "profile":
            response = {"user": UserSerializer(user).data, "orders": [], "order": {}}

        # if action == "remove":
        #     cartitem = cart.cartitems.get(product=product)
        #     print("cartitem", cartitem)
        #     # print(dir(cartitem))
        #     cartitem.delete()
        # else:
        #     cartitem, created_cartitem = cart.cartitems.get_or_create(product=product)
        #     cartitem.amount = product_amount
        #     cartitem.save()

        # serializer = CartSerializer(instance=cart)
        response["action"] = action
        return Response(
            response,
            status=status.HTTP_200_OK,
        )
