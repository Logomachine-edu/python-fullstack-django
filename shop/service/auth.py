from django.contrib.auth import authenticate, login
from django.http import HttpRequest

from django_logo.settings import EASY_LOGIN
from shop.models.customer import Customer


def authenticate_customer(request: HttpRequest, username, password) -> str:
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return "Authenticated successfully"
        return "Disabled account"
    if EASY_LOGIN:
        customer = Customer(username=username, password=password)
        customer.save()
        login(request, customer)
        return "Registered and authenticated successfully"
    return "Invalid login"
