from django import forms


class LoginForm(forms.Form):
    """Форма для логина."""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class AddToCartFrom(forms.Form):
    """Форма для добавления корзины."""

    item_info_id = forms.IntegerField(min_value=1)
    size = forms.CharField()
    color = forms.CharField()
    amount = forms.IntegerField(min_value=1)
