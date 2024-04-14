from dataclasses import dataclass
from decimal import Decimal

from django.db.models import Q

from shop.models import Customer, Item, ItemInfo, Order


@dataclass  # Больше по концепции подошел бы attrs =)
class CustomerService:
    """Сервис доступа к данным покупателя."""

    customer: Customer

    def get_cart(self) -> "Order":
        """Выдать покупателю корзину или создать новую и выдать."""
        if cart := self.customer.order_set.first():
            return cart
        # У покупателя всегда должна быть активная корзина.
        cart = Order(customer=self.customer)
        cart.save()
        return cart

    def get_orders(self) -> list["Order"]:
        return self.customer.order_set[1:]


@dataclass  # Больше по концепции подошел бы attrs =)
class CartService:
    """Сервис проведения операций с корзиной покупателя."""

    cart: "Order"

    def add_item(self, item_info: ItemInfo, color: str, size: str) -> None:
        """Добавить товар в корзину."""
        new_item = Item(cart=self, item_info=item_info, color=color, size=size)
        new_item.save()

    def add_item_copy(self, item: Item) -> None:
        """Увеличить количество копий товара на 1."""
        new_item = Item(cart=self, item_info=item.item_info, color=item.color, size=item.size)
        new_item.save()

    def delete_item_copy(self, item: Item) -> None:
        """Уменьшить количество копий товара на 1."""
        query_filter = Q(cart_pk=self.cart.pk, item_info__pk=item.item_info.pk, color=item.color, size=item.size)
        Item.objects.filter(pk__in=Item.objects.filter(query_filter).values_list("pk", flat=True)[0:1]).delete()

    def remove_all_item_copies(self, item: Item) -> None:
        """Удалить все копии товара."""
        query_filter = Q(cart_pk=self.cart.pk, item_info__pk=item.item_info.pk, color=item.color, size=item.size)
        Item.objects.filter(pk__in=Item.objects.filter(query_filter).values_list("pk", flat=True)).delete()

    def pay(self) -> None:
        """Оплатить заказ и создать новую пустую корзину."""
        if not self.cart.items:
            raise Exception("Sorry ... for what?")
        final_price = Decimal(0)
        for item in self.cart.items:
            item.final_price = item.current_price
            item.save()
            final_price += item.final_price
        self.cart.final_total_price = final_price
        self.cart.is_payed = True
        self.cart.save()
        Order(user=self.cart.customer).save()
