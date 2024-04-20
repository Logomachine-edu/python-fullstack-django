from dataclasses import dataclass
from decimal import Decimal

from django.db.models import Q
from django.db.models.fields.files import FieldFile

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


@dataclass
class ItemInCart:
    pk: int
    product_photo_file: FieldFile
    product_name: str
    price: Decimal
    quantity: int
    total: Decimal


@dataclass
class DetailedCart:
    items: list[ItemInCart]
    subtotal: Decimal
    shipping_price: Decimal
    total: Decimal


@dataclass  # Больше по концепции подошел бы attrs =)
class CartService:
    """Сервис проведения операций с корзиной покупателя."""

    cart: "Order"
    shipping_price: Decimal = Decimal(10)

    def __post_init__(self):
        if self.cart.is_payed:
            raise Exception("CartService is not available for payed orders.")

    def compose_detailed_info(self) -> DetailedCart:
        """Составить детальную информацию о заказе."""
        items: dict[int, ItemInCart] = {}
        subtotal = Decimal(0)

        items_map = self.cart.item_set.get_amount_per_item_info_map()
        for items_in_cart in items_map:
            items[items_in_cart["item_info"]] = ItemInCart(
                pk=items_in_cart["item_info"],
                product_photo_file=...,
                product_name=items_in_cart["item_info__name"],
                price=items_in_cart["item_info__price"],
                quantity=items_in_cart["quantity"],
                total=items_in_cart["total"],
            )

            subtotal += items_in_cart["total"]

        for item_info in ItemInfo.objects.get_catalog(Q(pk__in=items.keys())):
            items[item_info.pk].product_photo_file = item_info.title_photo

        return DetailedCart(
            items=list(items.values()),
            subtotal=subtotal,
            shipping_price=self.shipping_price,
            total=subtotal + self.shipping_price,
        )

    def add_item(self, item_info_id: int, color: str, size: str) -> None:
        """Добавить товар в корзину."""
        new_item = Item(order=self.cart, item_info_id=item_info_id, color=color, size=size)
        new_item.save()

    def add_item_copy(self, item: Item) -> None:
        """Увеличить количество копий товара на 1."""

    def delete_item_copy(self, item: Item) -> None:
        """Уменьшить количество копий товара на 1."""

    def remove_all_item_copies(self, item: Item) -> None:
        """Удалить все копии товара."""

    def pay(self) -> None:
        """Оплатить заказ и создать новую пустую корзину."""
        if not self.cart.item_set.count():
            raise Exception("Sorry ... for what?")
        final_price = Decimal(0)
        for item in self.cart.item_set.all():
            item.final_price = item.current_price
            item.save()
            final_price += item.final_price
        self.cart.final_total_price = final_price
        self.cart.is_payed = True
        self.cart.save()
        Order(user=self.cart.customer).save()
