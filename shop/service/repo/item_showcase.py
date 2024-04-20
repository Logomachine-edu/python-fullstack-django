"""
Реализация паттерна репозиторий через расширение менеджеров.

Подробнее:
    https://docs.djangoproject.com/en/5.0/topics/db/managers/
"""
from django.db import models
from django.db.models import Q


class ItemInfoQuerySet(models.QuerySet):
    @property
    def with_photos(self) -> models.QuerySet:
        return self.prefetch_related("photo_set")

    def get_trandy(self) -> list[models.Model]:
        """Список трендовых товаров на витрине."""
        return [self.form_aggregate(item_info) for item_info in self.with_photos.filter(is_trandy=True)]

    def get_catalog(self, filter_arg: Q | None = None) -> list[models.Model]:
        """Каталог товаров на витрине."""
        item_infos = self.with_photos.filter(filter_arg) if filter_arg else self.with_photos.all()
        return [self.form_aggregate(item_info) for item_info in item_infos]

    def get_aggregate(self, pk) -> models.Model:
        """Сборка агрегата models.ItemInfo."""
        if item_info := self.with_photos.filter(pk=pk).first():
            return self.form_aggregate(item_info)
        raise self.model.DoesNotExist

    @staticmethod
    def form_aggregate(item_info) -> models.Model:
        photos = list(item_info.photo_set.all())
        item_info._photos = photos
        return item_info

    get = get_aggregate


item_info_repository = ItemInfoQuerySet.as_manager()
