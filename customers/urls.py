from django.urls import path
from .views import RegisterCustomer

urlpatterns = [
    path('', RegisterCustomer.as_view(), name='customer_list'),
    path('register/', RegisterCustomer.as_view(), name='register'),
]

