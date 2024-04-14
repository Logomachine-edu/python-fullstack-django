"""
Реализация паттерна репозиторий через расширение менеджеров.

Подробнее:
    https://docs.djangoproject.com/en/5.0/topics/db/managers/
"""
from django.db import models


class CustomerQuerySet(models.QuerySet):
    @property
    def with_orders(self) -> models.QuerySet:
        return self.prefetch_related("order_set", "order_set__item_set", "order_set__item_set__item_info")

    def get_aggregate(self, pk):
        """Сборка агрегата models.Customer."""
        customer = self.with_orders.filter(pk=pk).first()
        return self.form_aggregate(customer)

    @staticmethod
    def form_aggregate(customer):
        orders = list(customer.order_set.all())
        customer.orders = orders
        return customer

    get = get_aggregate


customer_repository = CustomerQuerySet.as_manager()
