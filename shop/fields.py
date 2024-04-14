from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class PriceField(models.DecimalField):
    """Поле для хранения цены."""

    def __init__(
        self, verbose_name: str = None, name: str = None, max_digits: int = 12, decimal_places: int = 2, **kwargs
    ) -> None:
        if not kwargs.get("validators"):
            kwargs["validators"] = [MinValueValidator(Decimal("0.01"))]
        super().__init__(verbose_name, name, max_digits, decimal_places, **kwargs)
