"""Shop URLs."""
from django.urls import path

from shop import views

urlpatterns = [
    path("", views.ep_landing_page, name="landing_page"),
    path("items/", views.ep_items, name="items"),
    path("items/<int:item_id>/", views.ep_item_detail, name="item_detail"),
    path("cart/", views.ep_cart, name="cart"),
]
