# chat/urls.py
from django.conf.urls import url
from django.views.generic import TemplateView
from django.urls import path, include
from jobassistant.chat.views import (
    room_view
)

app_name = 'chat'

urlpatterns = [
    path('', TemplateView.as_view(template_name="chat/_chat_btn.html"), name='chat_btn'),
    url(r'^(?P<sender_uuid>[^/]+)/$', room_view, name='room'),
]
