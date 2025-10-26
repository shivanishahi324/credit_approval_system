from django.shortcuts import render

def home(request):
    return render(request, 'index.html')
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token

@requires_csrf_token
def csrf_debug_view(request, reason=""):
    return JsonResponse({
        "error": "CSRF verification failed",
        "reason": reason,
        "csrf_cookie": request.COOKIES.get('csrftoken'),
        "csrf_meta": request.META.get('CSRF_COOKIE')
    }, status=403)

