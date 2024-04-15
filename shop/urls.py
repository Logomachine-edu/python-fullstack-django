"""Shop URLs."""
from django.urls import path

from shop import views

urlpatterns = [
    path("login/", views.ep_login, name="login_page"),
    path("", views.LandingPageView.as_view(), name="landing_page"),
    path("items/", views.ItemsView.as_view(), name="items"),
    path("items/<int:item_id>/", views.ItemDetailView.as_view(), name="item_detail"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/add_item", views.AddItemToCart.as_view(), name="add_item_to_cart"),
]
