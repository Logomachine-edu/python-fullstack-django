from django import forms


class LoginForm(forms.Form):
    """Форма для логина."""

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
