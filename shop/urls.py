from django.urls import path
from .views import ShopView,ShopDetailView,ProductCreateView,ProductUpdateView,ProductDeleteView,AddToCartView,CartView,UpdateCountOfCart,DeleteCart
urlpatterns = [
    path("", ShopView.as_view(), name="shop"),
    path("add-to-cart/", AddToCartView.as_view(), name="add-to-cart"),
    path("update-cart/", UpdateCountOfCart.as_view(), name="update-cart"),
    path("delete-cart/", DeleteCart.as_view(), name="delete-cart"),
    path("cart/", CartView.as_view(), name="cart"),
    path("<int:id>/", ShopDetailView.as_view(), name="shop-detail"),
    path("create/", ProductCreateView.as_view(), name="shop-create"),
    path("update/<int:id>/", ProductUpdateView.as_view(), name="shop-update"),
    path("delete/<int:id>/", ProductDeleteView.as_view(), name="shop-delete"),
]
