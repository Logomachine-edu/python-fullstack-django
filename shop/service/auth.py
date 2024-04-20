from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.db import IntegrityError
from django.http import HttpRequest

from django_logo.settings import EASY_LOGIN
from shop.models.order import Customer


def authenticate_customer(request: HttpRequest, username: str, password: str) -> tuple[bool, str]:
    """Аутентификация покупателя.

    Возвращаем флаг успешности и текст сообщения.
    """
    user = authenticate(request=request, username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request=request, user=user)
            return True, "Authenticated successfully"
        return False, "Disabled account"
    if EASY_LOGIN:
        customer = Customer(username=username, password=make_password(password))
        try:
            customer.save()
        except IntegrityError:
            return False, "Invalid password"
        login(request, customer)
        return True, "Registered and authenticated successfully"
    return False, "Invalid login"
