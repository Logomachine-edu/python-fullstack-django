from django.http import HttpRequest, HttpResponse, StreamingHttpResponse
from django.template.response import TemplateResponse


class FullMiddlewareProtocol:
    """Протокол Middleware Django, заряженный всеми возможными к обращению при обработке запроса методами.

    Не подлежит наследованию, тк в порядке оптимизации у Middleware стоит держать только полезные методы.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Блок, заменяющий process_request в версиях 1.10+
        response = self.get_response(request)
        #  Блок, заменяющий process_response в версиях 1.10+
        return response

    # Порядок прямой
    def process_request(self, request: HttpRequest) -> HttpResponse | None:
        """Deprecated в версии Django 5.

        Этап 1. Обработка объекта запроса (HttpRequest) из WSGI.
        При возврате HttpResponse обработка запроса прекратится и клиент получит ответ согласно данному HttpResponse.
        """

    def process_view(self, request: HttpRequest, view_func, view_args, view_kwargs) -> HttpResponse | None:
        """Этап 2. Обработка HttpRequest после роутинга и подбора соответствующего View.

        При возврате HttpResponse обработка запроса прекратится и клиент получит ответ согласно данному HttpResponse.
        """

    # Порядок обратный
    def process_exception(self, request: HttpRequest, exception: Exception) -> HttpResponse | None:
        """Этап 3а. Обработка HttpRequest при вызове исключения в View.

        При возврате HttpResponse обработка запроса прекратится и клиент получит ответ согласно данному HttpResponse.
        """

    def process_template_response(self, request: HttpRequest, response: TemplateResponse) -> TemplateResponse:
        """Этап 3б. Обработка HttpRequest при необходимости рендерить шаблон (View вернул TemplateResponse).

        Между Middleware с методами process_template_response будет передаваться TemplateResponse,
            поэтому этот метод обязательно должен возвращать именно его.
        """

    def process_response(
        self, request: HttpRequest, response: HttpResponse | StreamingHttpResponse
    ) -> HttpResponse | StreamingHttpResponse:
        """Deprecated в версии Django 5!

        Этап 3в. Обработка HttpRequest и генерация ответа.
        Между Middleware с методами process_response будет передаваться HttpResponse | StreamingHttpResponse,
            поэтому этот метод обязательно должен возвращать именно его.
        """
