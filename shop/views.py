from django.http import HttpResponseNotAllowed, HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.
# Docs: https://docs.djangoproject.com/en/5.0/ref/class-based-views/base/


def ep_landing_page(request: HttpRequest) -> HttpResponse:
    """Эндпоинт для отобрадения лендинга."""
    if request.method == "GET":
        return render(request, "shop/landing_page.html")
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


def ep_items(request: HttpRequest) -> HttpResponse:
    """Эндпоинт для отображения товаров."""
    if request.method == "GET":
        context = {"items": range(1, 10)}
        return render(request, "shop/items.html", context=context)
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


def ep_item_detail(request: HttpRequest, item_id: int) -> HttpResponse:
    """Эндпоинт для отображения детальной информации о товаре."""
    if request.method == "GET":
        return render(request, "shop/item_detail.html")
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])


def ep_cart(request: HttpRequest) -> HttpResponse:
    """Эндпоинт для отображения корзины."""
    if request.method == "GET":
        return render(request, "shop/cart.html")
    else:
        return HttpResponseNotAllowed(permitted_methods=["GET"])
