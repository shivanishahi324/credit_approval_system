"""
URL configuration for credit_approval project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.http import JsonResponse

# def home(request):
#     return JsonResponse({"message": " Credit Approval API is running successfully!"})

from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views 


urlpatterns = [
    path('', views.home, name='home'), 
    path('admin/', admin.site.urls),
    path('api/v1/', include('customers.urls')),
    path('api/v1/', include('loans.urls')),
    path('csrf-test/', views.csrf_debug_view),
    path('csrf-test/', views.csrf_debug_view),


]
