from django.conf.urls import url
from django.views.generic import TemplateView
from django.urls import path, include

from jobassistant.dashboard.views import (
    dashboard_menu,
    dashboard_main_view
)

app_name = 'dashboard'

urlpatterns = [
    path('',
         dashboard_main_view,
         name='dashboard'),
    path('dashboard_menu/',
         dashboard_menu,
         name='dashboard-menu'),
]
