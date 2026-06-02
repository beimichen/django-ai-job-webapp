from django.contrib.auth import get_user_model
from django.forms import formset_factory, ModelForm, inlineformset_factory, modelformset_factory
from django.forms.models import fields_for_model
from django.forms import BaseModelFormSet
from django import forms

# Third Party
from bootstrap_datepicker_plus import DatePickerInput
from dal import autocomplete
from djangoformsetjs.utils import formset_media_js
# from phonenumber_field import formfields
# from phonenumber_field.widgets import PhoneNumberPrefixWidget


# Models
from .models import *

User = get_user_model()

datetimepicker_css_1 = (
    "css/bootstrap-datetimepicker.min.css",
    "css/datepicker-widget.css",
)

datetimepicker_css = (
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.47/css/bootstrap-datetimepicker.css",
)

taggit_selectize_css = (
    "taggit_selectize/css/selectize.django.css",
    "admin/css/autocomplete.css",
    "autocomplete_light/select2.css",
)

taggit_selectize_js = (
    "taggit_selectize/js/selectize.js",
)

selectize_css = (
    "admin/css/vendor/select2/select2.css",
    "admin/css/autocomplete.css",
    "autocomplete_light/select2.css",
)

selectize_js = (
    "autocomplete_light/jquery.init.js",
    "autocomplete_light/autocomplete.init.js",
    "autocomplete_light/forward.js",
    "autocomplete_light/select2.js",
    "autocomplete_light/jquery.post-setup.js",
)

formset_js = (
    # "js/jquery.formset.js",
    "js/jquery.formset.min.js",
)

formset_js_remote = (
    "https://cdnjs.cloudflare.com/ajax/libs/jquery.formset/1.2.2/jquery.formset.min.js",
    )

experience_js = (
    "js/resume_experiences.min.js",
)

chainedfk_js = (
    "smart-selects/admin/js/chainedfk.js",
    "smart-selects/admin/js/bindfields.js",
)

datetimepicker_js_1 = (
    "js/moment-with-locales.min.js",
    "js/bootstrap-datetimepicker.min.js",
    "js/datepicker-widget-v1.js",
)

# experience_js = (
#     "js/jquery.formset.min.js",
#     "js/moment-with-locales-v1.min.js",
#     "js/bootstrap-datetimepicker.min.js",
#     "js/datepicker-widget-v1.js",
#     "js/jquery.init.js",a
#     "js/autocomplete.init.js",
#     "js/forward.js",
#     "js/select2.js",
#     "js/jquery.post-setup.js",
#     "js/chainedfk.js",
#     "js/bindfields.js",
#     "js/resume_experiences.min.js",
# )


education_formset_js = (
    "js/chainedfk.js",
    "js/bindfields.js",
    "js/moment-with-locales-v1.min.js",
    "js/bootstrap-datetimepicker-v1.min.js",
    "js/datepicker-widget-v1.js",
    "js/resume_experiences.min.js",
    "js/jquery.formset.min.js",
    "js/jquery.init.js",
    "js/autocomplete.init.js",
    "js/forward.js",
    "js/select2.js",
    "js/jquery.post-setup.js",
)

datetimepicker_js = (
    "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.9.0/moment-with-locales.min.js",
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.47/js/bootstrap-datetimepicker.min.js",
)


class CreatePersonal(forms.ModelForm):
    class Meta:
        model = Personal
        exclude = ['parent_user', 'complete_status']

    class Media(object):
        js = taggit_selectize_js
        css = taggit_selectize_css


class CreateLanguage(ModelForm):
    class Meta:
        model = Language
        exclude = ['personal']

    class Media(object):
        js = taggit_selectize_js
        css = taggit_selectize_css


PersonalFormSet = inlineformset_factory(Personal,
                                        Language,
                                        form=CreateLanguage,
                                        extra=1,
                                        )


class ManageExperience(ModelForm):
    position = forms.ModelChoiceField(
        queryset=Positions.objects.all(),
        widget=autocomplete.ModelSelect2(url='resume:positions-autocomplete')
    )
    # company = forms.ModelChoiceField(
    #     queryset=Companies.objects.all(),
    #     widget=autocomplete.ModelSelect2(url='resume:companies_autocomplete')
    # )
    company = forms.CharField(label='Company', max_length=150)

    def clean_title(self):
        return self.cleaned_data['company'].title()

    class Media(object):
        js = experience_js + datetimepicker_js_1 + formset_js

        css = {
            "selectize": selectize_css,
            "datetimepicker": datetimepicker_css_1,
        }

    class Meta:
        model = Experience
        exclude = ['candidate', 'complete_status']
        fields = ('__all__')
        widgets = {
            'work_start_date': DatePickerInput(),
            'work_end_date': DatePickerInput(),
        }


ExperienceFormSet = modelformset_factory(model=Experience,
                                         form=ManageExperience,
                                         exclude=['candidate', 'complete_status'],
                                         extra=1,)


class ManageEducation(ModelForm):
    institution = forms.ModelChoiceField(
        queryset=EducationInstitutions.objects.all(),
        widget=autocomplete.ModelSelect2(url='resume:institutions-autocomplete')
    )

    class Media(object):
        js = experience_js + datetimepicker_js_1  + formset_js # experience_js  + formset_js + datetimepicker_js_1  # formset_js + datetime_picker_js + selectize_js
        css = {
            "selectize": selectize_css,
            "datetimepicker": datetimepicker_css_1,
        }

    class Meta:
        model = Education
        exclude = ['candidate', 'complete_status']
        fields = ('__all__')
        widgets = {
            'education_start_date': DatePickerInput(),
            'education_end_date': DatePickerInput(),
        }


EducationFormSet = modelformset_factory(model=Education,
                                        form=ManageEducation,
                                        exclude=['candidate', 'complete_status'],)


class CreateReference(ModelForm):
    current_position = forms.ModelChoiceField(
        queryset=Positions.objects.all(),
        widget=autocomplete.ModelSelect2(url='resume:positions-autocomplete')
    )

    class Media(object):
        js = formset_js
        css = {
            "selectize": selectize_css
        }

    class Meta:
        model = Reference
        exclude = ['candidate', 'complete_status']
        fields = ('__all__')


ReferenceFormSet = modelformset_factory(model=Reference,
                                        form=CreateReference,
                                        exclude=['candidate', 'complete_status'],)
