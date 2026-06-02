from django.urls import path

from jobassistant.users.views import (
    user_list_view,
    user_redirect_view,
    user_update_view,
    user_detail_view,
    user_create_view,
    user_register_view,
)

app_name = "users"
urlpatterns = [
    path("signup/", view=user_create_view, name="signup"),
    path("register/", view=user_register_view, name="register"),
    path("", view=user_list_view, name="list"),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
