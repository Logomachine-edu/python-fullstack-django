from datetime import datetime
from decimal import Decimal

from django.db import models

from shop.fields import PriceField
from shop.service.repo.item_info import item_info_repository


class ItemInfo(models.Model):
    """Информация о товаре на витрине."""

    is_trandy: bool = models.BooleanField(default=False, help_text="Whether the item is included in trandy list.")
    name: str = models.CharField(max_length=255)
    price: Decimal = PriceField()
    old_price: Decimal = PriceField(null=True, blank=True, default=None)
    summary: str = models.CharField(max_length=255)
    description: str = models.TextField(blank=True)
    additional_information: str = models.TextField(null=True, blank=True)

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    photos: list["ItemsPhoto"]  # Доступно при вызове form_aggregate
    photo_set: models.Manager["ItemsPhoto"]  # RelatedManager
    objects = item_info_repository  # Расширенный Manager

    def __str__(self):
        return f"ItemInfo {self.name}"

    @property
    def title_photo(self):
        """Титульное фото товара."""
        photo = self.photos[0]
        return photo.file if photo else "-"


class ItemsPhoto(models.Model):
    """Фотография товара."""

    def get_file_path(self, filename: str) -> str:
        """Генерация пути файла."""
        return f"items_photos/{self.item_info.pk}/{filename}"

    file = models.ImageField(upload_to=get_file_path)
    item_info: "ItemInfo" = models.ForeignKey(
        "shop.ItemInfo", on_delete=models.CASCADE, related_name="photo_set", related_query_name="photo_set"
    )

    created_at: datetime = models.DateTimeField(auto_now_add=True)
    updated_at: datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Photo {self.file.name} for {self.item_info}"
