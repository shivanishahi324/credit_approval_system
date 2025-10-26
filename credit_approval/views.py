from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

@requires_csrf_token
def csrf_debug_view(request, reason=""):
    return JsonResponse({
        "error": "CSRF verification failed ❌",
        "reason": reason,
        "origin": request.META.get("HTTP_ORIGIN"),
        "referer": request.META.get("HTTP_REFERER"),
        "csrf_cookie": request.COOKIES.get("csrftoken"),
        "csrf_meta": request.META.get("CSRF_COOKIE"),
    }, status=403)
