"""
Реализация паттерна репозиторий через расширение менеджеров.

Подробнее:
    https://docs.djangoproject.com/en/5.0/topics/db/managers/
"""
from decimal import Decimal
from typing import TypedDict

from django.contrib.auth.models import UserManager
from django.db import models
from django.db.models import Count, Sum


class CustomerQuerySet(models.QuerySet):
    @property
    def with_orders(self) -> models.QuerySet:
        return self.prefetch_related("order_set")

    def get_aggregate(self, *args, **kwargs):
        """Сборка агрегата models.Customer."""
        if customer := self.with_orders.filter(*args, **kwargs).first():
            return self.form_aggregate(customer)
        raise self.model.DoesNotExist

    @staticmethod
    def form_aggregate(customer):
        orders = list(customer.order_set.all())
        customer._orders = orders
        return customer

    get = get_aggregate


class CustomerManager(UserManager.from_queryset(CustomerQuerySet)):
    """Репозиторий для работы с покупателями.

    Перегружаем таким образом, чтобы сохранить методы из базового UserManager.
    """


customer_repository = CustomerManager()


class AmountPerItemInfoMap(TypedDict):
    """Элемент результата запроса ItemQuerySet.get_amount_per_item_info_map."""

    item_info: int  # Первичный ключ
    item_info__name: str
    item_info__price: Decimal
    quantity: int
    total: Decimal


class ItemQuerySet(models.QuerySet):
    def get_current_total_price(self) -> Decimal:
        """Совокупная цена за товары в заказе на данный момент."""
        return self.aggregate(Sum("item_info__price", default=Decimal(0)))

    def get_amount_per_item_info_map(self) -> models.QuerySet[AmountPerItemInfoMap]:
        """Соответствие первичных ключей товаров на витрине и их количества в заказе."""
        base_query = self.values("item_info", "item_info__price", "item_info__name")
        return base_query.annotate(quantity=Count("item_info"), total=Sum("item_info__price")).order_by("item_info")


item_repository = ItemQuerySet.as_manager()
