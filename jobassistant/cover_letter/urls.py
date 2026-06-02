# resume/urls.py
from django.conf.urls import url
from django.urls import path, include

from jobassistant.cover_letter.views import (
    cover_letter_list,
    # create_cover_letter,
    update_cover_letter,
)

app_name = 'cover_letter'

urlpatterns = [
    # path('',
    #      create_cover_letter,
    #      name='create-cover-letter'),
    url(r'(?P<pk>[0-9]+)/$',
        update_cover_letter,
        name='update-cover-letter'),
    path('list/',
         cover_letter_list,
         name='cover-letter-list'),
]
