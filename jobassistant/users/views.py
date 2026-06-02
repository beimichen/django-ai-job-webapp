from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView, ListView, RedirectView, UpdateView, CreateView, FormView
from django.middleware.csrf import get_token
from .forms import UserCreationForm


from bootstrap_modal_forms.mixins import PassRequestMixin
# from allauth.account.views import SignupView


User = get_user_model()


class UserCreateView(PassRequestMixin, SuccessMessageMixin, CreateView):
    template_name = 'account/signup.html'
    form_class = UserCreationForm
    # success_message = "Success: You've signed up!"
    # success_url = reverse_lazy('users:signup') # TODO: change to createview like so: https://stackoverflow.com/questions/28791438/how-i-can-prevent-createview-django-1-6-redirect-me-to-the-success-url-if-the
                                                 # TODO: register/login user here within form_valid method


user_create_view = UserCreateView.as_view()


# register user after sign up
def register(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    new_user = authenticate(username=username, password=password)
    login(request, new_user, backend='allauth.account.auth_backends.AuthenticationBackend')
    print(request.user)
    return JsonResponse({'data': 'success'})


user_register_view = register


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserListView(LoginRequiredMixin, ListView):

    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_list_view = UserListView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()



