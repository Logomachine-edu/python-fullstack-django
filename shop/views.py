from typing import Type

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView

from shop.forms import LoginForm
from shop.models import ItemInfo
from shop.models.customer import Customer, Order
from shop.service.auth import authenticate_customer
from shop.service.handlers.customer import CustomerService


def ep_login(request: HttpRequest) -> HttpResponse:
    """Эндпоинт для описания страницы входа в аккаунт."""
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            auth_result = authenticate_customer(request, cleaned_data["username"], cleaned_data["password"])
            return HttpResponse(auth_result)
    else:
        form = LoginForm()
    return render(request, "shop/login.html", {"form": form})


class BaseShopView(TemplateView):
    request: HttpRequest
    customer_service: CustomerService

    def setup(
        self, request: HttpRequest, *args, customer_service_cls: Type[CustomerService] = CustomerService, **kwargs
    ):
        """Реализация паттерна Инъекция зависимостей - поставляем сервисы в представление."""
        self._ensure_authentication(request)  # Сначала удостоверимся, что покупатель аутентифицирован

        super().setup(request, *args, **kwargs)
        customer: Customer = request.user
        self.customer_service = customer_service_cls(customer=customer)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.customer_service.get_cart()
        return context | dict(cart=cart)

    @staticmethod
    def _ensure_authentication(request: HttpRequest):
        if request.user.is_anonymous:
            return HttpResponseRedirect("login/")


class LandingPageView(BaseShopView):
    template_name = "shop/landing_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trandy_item_infos = ItemInfo.objects.get_trandy()
        return context | dict(trandy_item_infos=trandy_item_infos)


class ItemsView(BaseShopView):
    template_name = "shop/items.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_infos = ItemInfo.objects.get_catalog()
        return context | dict(item_infos=item_infos)


class ItemDetailView(BaseShopView):
    template_name = "shop/item_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        item_id: int = kwargs["item_id"]
        item_info = ItemInfo.objects.get_aggregate(pk=item_id)
        return context | dict(item_info=item_info)


class CartView(BaseShopView):
    template_name = "shop/cart.html"
