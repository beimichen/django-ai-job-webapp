from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms.models import fields_for_model


from bootstrap_modal_forms.mixins import PopRequestMixin, CreateUpdateAjaxMixin

User = get_user_model()


class UserChangeForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.UserChangeForm):

    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(PopRequestMixin, CreateUpdateAjaxMixin, forms.UserCreationForm):

    error_messages = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta(forms.UserCreationForm.Meta):
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def save(self, commit=False):
        if not self.request.is_ajax():
            instance = super(CreateUpdateAjaxMixin, self).save(commit=commit)
            instance.save()
        else:
            instance = super(CreateUpdateAjaxMixin, self).save(commit=False)
        return instance

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(self.error_messages["duplicate_username"])
