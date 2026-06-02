from django.contrib import admin
from django.urls import path

from .views import contact, success_contact

urlpatterns = [
    path('email/', contact, name='email'),
    path('success/', success_contact, name='success'),
]
