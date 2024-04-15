from typing import Type

from django.db.transaction import atomic
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView

from shop.forms import AddToCartFrom, LoginForm
from shop.models import ItemInfo
from shop.models.customer import Customer
from shop.service.auth import authenticate_customer
from shop.service.handlers.customer import CartService, CustomerService


def ep_login(request: HttpRequest) -> HttpResponse:
    """Эндпоинт для описания страницы входа в аккаунт."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            auth_result = authenticate_customer(request, cleaned_data["username"], cleaned_data["password"])
            return redirect(to=request.headers["Referer"] or "/")
    else:
        form = LoginForm()
    return render(request, "shop/login.html", {"form": form})


class BaseShopView(View):
    request: HttpRequest
    customer_service: CustomerService

    def setup(
        self, request: HttpRequest, *args, customer_service_cls: Type[CustomerService] = CustomerService, **kwargs
    ):
        """Реализация паттерна Инъекция зависимостей - поставляем сервисы в представление."""
        super().setup(request, *args, **kwargs)
        if request.user.is_anonymous:  # Сначала удостоверимся, что покупатель аутентифицирован
            self.get = self._login_regirect
        customer: Customer = request.user
        self.customer_service = customer_service_cls(customer=customer)

    @staticmethod
    def _login_regirect(request: HttpRequest, *args, **kwargs):
        return redirect("login_page")


class BaseShopTemplateView(BaseShopView, TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.customer_service.get_cart()
        total_items_in_cart = cart.item_set.count()
        return context | dict(cart=cart, total_items_in_cart=total_items_in_cart)


class LandingPageView(BaseShopTemplateView):
    template_name = "shop/landing_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trandy_item_infos = ItemInfo.objects.get_trandy()
        return context | dict(trandy_item_infos=trandy_item_infos)


class ItemsView(BaseShopTemplateView):
    template_name = "shop/items.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_infos = ItemInfo.objects.get_catalog()
        return context | dict(item_infos=item_infos)


class ItemDetailView(BaseShopTemplateView):
    template_name = "shop/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id: int = kwargs["item_id"]
        item_info = ItemInfo.objects.get_aggregate(pk=item_id)
        return context | dict(item_info=item_info)


class CartView(BaseShopTemplateView):
    template_name = "shop/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        detailed_cart = CartService(cart=context["cart"]).compose_detailed_info()
        return context | dict(detailed_cart=detailed_cart)


class BaseCartOperationsView(BaseShopView):
    cart_service: CartService

    def setup(
        self,
        request: HttpRequest,
        *args,
        customer_service_cls: Type[CustomerService] = CustomerService,
        cart_service_cls: Type[CartService] = CartService,
        **kwargs
    ):
        """Реализация паттерна Инъекция зависимостей - поставляем сервисы в представление."""
        super().setup(request, customer_service_cls=customer_service_cls, *args, **kwargs)
        cart = self.customer_service.get_cart()
        self.cart_service = cart_service_cls(cart=cart)


class AddItemToCart(BaseCartOperationsView):
    @atomic
    def post(self, request: HttpRequest):
        form = AddToCartFrom(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            for _ in range(cleaned_data["amount"]):
                self.cart_service.add_item(
                    item_info_id=cleaned_data["item_info_id"], color=cleaned_data["color"], size=cleaned_data["size"]
                )
        return redirect(to=request.headers["Referer"] or "/")
