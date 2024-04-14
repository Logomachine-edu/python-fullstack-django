from datetime import datetime
from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum

from shop.fields import PriceField
from shop.service.repo.customer import customer_repository


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

    items_set: models.Manager["Item"]  # RelatedManager

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        label = "Order" if self.is_payed else "Cart"
        return f"{label} for {self.customer}"

    def get_current_total_price(self) -> Decimal:
        """Совокупная цена за товары в заказе на данный момент."""
        return self.items_set.aggregate(Sum("item_info__price", default=0))

    def get_total_items(self) -> int:
        """Количество товаров в заказе."""
        return self.items_set.count()


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
    cart = models.ForeignKey("shop.Order", on_delete=models.CASCADE)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    @property
    def current_price(self) -> Decimal:
        """Текущая цена."""
        return self.item_info.price
