from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models

from shop.fields import PriceField
from shop.service.repo.customer import customer_repository, item_repository


class Customer(AbstractUser):
    """Покупатель."""

    orders: list["Order"]  # Доступно при вызове form_aggregate
    order_set: models.Manager["Order"]  # RelatedManager
    objects = customer_repository  # Расширенный Manager


class Order(models.Model):
    """Заказ."""

    is_payed: bool = models.BooleanField(default=False)
    shipping_price: Decimal = PriceField(default=Decimal(10))
    final_total_price: Decimal | None = PriceField(default=None, null=True)
    customer = models.ForeignKey("shop.Customer", on_delete=models.CASCADE)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    item_set: item_repository  # RelatedManager >> item_repository

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        label = "Order" if self.is_payed else "Cart"
        return f"{label} for {self.customer}"


class Item(models.Model):
    """Конкретный товар."""

    size: str = models.CharField(max_length=3, choices=models.TextChoices("ItemSize", "XS S M L XL"))
    color: str = models.CharField(max_length=16, choices=models.TextChoices("ItemColor", "Black White Red Blue Green"))
    final_price: Decimal | None = PriceField(default=None, null=True, blank=True)
    item_info = models.ForeignKey(
        "shop.ItemInfo",
        on_delete=models.CASCADE,
        related_name="+",  # Не даем создавать обратную связь
        related_query_name="+",  # Не даем создавать обратную связь
    )
    order = models.ForeignKey("shop.Order", on_delete=models.CASCADE)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    objects = item_repository  # Расширение Manager

    def __str__(self):
        return f"Item {self.item_info} for {self.order}"

    @property
    def current_price(self) -> Decimal:
        """Текущая цена."""
        return self.item_info.price
