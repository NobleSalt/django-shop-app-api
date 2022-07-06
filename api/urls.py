from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from api.views import (
    CartAction,
    FetchCart,
    category_list,
    create_store,
    get_login,
    get_product_by_id,
    get_user,
    index,
    product_list,
    product_seller,
    products_by_category,
    search_product,
)

app_name = "api"

urlpatterns = [
    path("", index, name="home"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.authtoken")),
    # path("auth-djoser/", include("djoser.urls"), name="auth-djooser"),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),  # <-- And here
    path("product_list/", product_list),
    path("category_list/", category_list),
    path("get_product_by_id/<id>/", get_product_by_id),
    path("products_by_category/<category>/", products_by_category),
    path("product_seller/<id>/", product_seller),
    path("get_user/<id>/", get_user),
    path("product_seller/<id>/", product_seller),
    path("get_login/<email>/", get_login),
    path("search_product/", search_product.as_view()),
    path("fetch_cart/", FetchCart.as_view()),
    path("cart_action/", CartAction.as_view()),
    # path('get_login/<email>/', get_login),
    # path('products/', product_list),
]
