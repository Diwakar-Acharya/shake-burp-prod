"""Custom middleware that renders our branded 404/403/500 pages even in DEBUG mode."""

from django.shortcuts import render


class CustomErrorMiddleware:
    """
    In DEBUG=True mode, Django bypasses handler404/500 and shows its own debug pages.
    This middleware intercepts those responses and swaps in our custom error templates.
    In production (DEBUG=False), Django's standard handler404 / handler500 mechanism
    already uses our handler, so this middleware passes through.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.conf import settings
        response = self.get_response(request)

        # Only intercept in DEBUG mode — in production Django already uses handler404
        if settings.DEBUG:
            if response.status_code == 404:
                response = render(request, '404.html', {'page': 'error'}, status=404)
            elif response.status_code == 403:
                response = render(request, '403.html', {'page': 'error'}, status=403)
            elif response.status_code == 500:
                response = render(request, '500.html', {'page': 'error'}, status=500)

        return response
