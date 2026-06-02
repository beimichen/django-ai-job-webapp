# Django components
# from django.shortcuts import render, redirect, render_to_response, HttpResponseRedirect
from django.contrib.auth.models import Permission
# from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic.edit import FormView, CreateView, UpdateView
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Serializer and model
from jobassistant.resume.serializers import *

# Forms and Models
from .models import *
from .forms import *

# Third Party
from bootstrap_datepicker_plus import DatePickerInput
from extra_views import *
from braces import views
from dal import autocomplete
from rest_framework import viewsets, generics
from datetime import date

# rest framework
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from compressor.base import Compressor
from compressor.exceptions import (CompressorError, UncompressableFileError,
        FilterDoesNotExist)


class CustomCompressor(object):

    def __init__(self, *args, **kwargs):
            super(CustomCompressor, self).__init__(*args, **kwargs)

    def get_basename(self, url):
        """
        Takes full path to a static file (eg. "/static/css/style.css") and
        returns path with storage's base url removed (eg. "css/style.css").
        """
        if url == "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.47/css/bootstrap-datetimepicker.css":
            try:
                base_url = self.storage.base_url
            except AttributeError:
                base_url = settings.COMPRESS_URL

            url = base_url + 'css/bootstrap-datetimepicker.min.css'
            if not url.startswith(base_url):
                raise UncompressableFileError("'%s' isn't accessible via "
                                              "COMPRESS_URL ('%s') and can't be "
                                              "compressed" % (url, base_url))
            basename = url.replace(base_url, "", 1)
            # drop the querystring, which is used for non-compressed cache-busting.
            return basename.split("?", 1)[0]
        elif url == "https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.9.0/moment-with-locales.min.js":
            try:
                base_url = self.storage.base_url
            except AttributeError:
                base_url = settings.COMPRESS_URL

            url = base_url + 'js/moment-with-locales.min.js'
            if not url.startswith(base_url):
                raise UncompressableFileError("'%s' isn't accessible via "
                                              "COMPRESS_URL ('%s') and can't be "
                                              "compressed" % (url, base_url))
            basename = url.replace(base_url, "", 1)
            # drop the querystring, which is used for non-compressed cache-busting.
            return basename.split("?", 1)[0]
        elif url == "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datetimepicker/4.17.47/js/bootstrap-datetimepicker.min.js":
            try:
                base_url = self.storage.base_url
            except AttributeError:
                base_url = settings.COMPRESS_URL

            url = base_url + 'js/bootstrap-datetimepicker.min.js'
            if not url.startswith(base_url):
                raise UncompressableFileError("'%s' isn't accessible via "
                                              "COMPRESS_URL ('%s') and can't be "
                                              "compressed" % (url, base_url))
            basename = url.replace(base_url, "", 1)
            # drop the querystring, which is used for non-compressed cache-busting.
            return basename.split("?", 1)[0]
        elif url == "https://ajax.googleapis.com/ajax/libs/jquery/2.2.0/jquery.min.js":
            try:
                base_url = self.storage.base_url
            except AttributeError:
                base_url = settings.COMPRESS_URL

            url = base_url + 'js/jquery.min.js'
            if not url.startswith(base_url):
                raise UncompressableFileError("'%s' isn't accessible via "
                                              "COMPRESS_URL ('%s') and can't be "
                                              "compressed" % (url, base_url))
            basename = url.replace(base_url, "", 1)
            # drop the querystring, which is used for non-compressed cache-busting.
            return basename.split("?", 1)[0]
        else:
            try:
                base_url = self.storage.base_url
            except AttributeError:
                base_url = settings.COMPRESS_URL
            if not url.startswith(base_url):
                raise UncompressableFileError("'%s' isn't accessible via "
                                              "COMPRESS_URL ('%s') and can't be "
                                              "compressed" % (url, base_url))
            basename = url.replace(base_url, "", 1)
            # drop the querystring, which is used for non-compressed cache-busting.
            return basename.split("?", 1)[0]

Compressor.get_basename = CustomCompressor.get_basename


class NeverCacheMixin(object):
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        return super(NeverCacheMixin, self).dispatch(*args, **kwargs)


User = get_user_model()


class PositionsAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Positions.objects.all()
        if self.q:
            qs = qs.filter(positions__istartswith=self.q)
        return qs


positions_autocomplete = PositionsAutocomplete.as_view(create_field='positions')


class CompaniesAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Companies.objects.all()
        if self.q:
            qs = qs.filter(companies__istartswith=self.q)
        return qs


companies_autocomplete = CompaniesAutocomplete.as_view(create_field='companies')


class EducationInstitutionsAutocomplete(LoginRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = EducationInstitutions.objects.all()
        if self.q:
            qs = qs.filter(institutions__istartswith=self.q)
        return qs


education_institutions_autocomplete = EducationInstitutionsAutocomplete.as_view(create_field='institutions')


class PersonalList(ListView):
    model = Personal
    template_name = 'resume/resume_form_list.html'


personal_list = PersonalList.as_view()


class CreateResumePersonalView(LoginRequiredMixin, CreateView):
    model = Personal
    fields = ['first_name', 'middle_name', 'last_name', 'address', 'city', 'state', 'zip_code', 'country',
              'email', 'phone', 'profile_summary', 'skills', 'tools']
    exclude = ['parent_user', 'complete_status']
    template_name = 'resume/resume_form_personal.html'
    success_url = reverse_lazy('resume:experiences')

    def get_context_data(self, **kwargs):
        data = super(CreateResumePersonalView, self).get_context_data(**kwargs)

        if self.request.POST:
            data['languages'] = PersonalFormSet(self.request.POST)
        else:
            data['languages'] = PersonalFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        languages = context['languages']
        if form.is_valid():
            personal = form.save(commit=False)
            personal.parent_user = self.request.user
            personal.save()
            if None not in (form['first_name'].value(), form['last_name'].value(),
                            # form['address'].value(), form['city'].value(), form['state'].value(),
                            # form['zip_code'].value(), form['country'].value(),
                            form['phone'].value(), form['email'].value(), form['profile_summary'].value(),
                            form['skills'].value(), form['tools'].value()):
                personal.complete_status = True
            with transaction.atomic():
                self.object = form.save(commit=False)
                if languages.is_valid():
                    languages.instance = self.object
                    # languages.parent_user = self.request.user
                    languages.save()
            return super(CreateResumePersonalView, self).form_valid(form)


create_personal_resume_form = CreateResumePersonalView.as_view()


class UpdateResumePersonalView(LoginRequiredMixin, UpdateView):
    model = Personal
    fields = ['first_name', 'middle_name', 'last_name', 'address', 'city', 'state', 'zip_code', 'country',
              'email', 'phone', 'profile_summary', 'skills', 'tools']
    exclude = ['parent_user', 'complete_status']
    template_name = 'resume/resume_form_personal.html'
    success_url = reverse_lazy('resume:experiences')

    def get_context_data(self, **kwargs):
        data = super(UpdateResumePersonalView, self).get_context_data(**kwargs)
        if self.request.POST:
            data['languages'] = PersonalFormSet(self.request.POST, instance=self.object)
        else:
            data['languages'] = PersonalFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        languages = context['languages']
        if form.is_valid():
            personal = form.save(commit=False)
            personal.save()
            if None not in (form['first_name'].value(), form['last_name'].value(),
                            # form['address'].value(), form['city'].value(), form['state'].value(),
                            # form['zip_code'].value(), form['country'].value(),
                            form['phone'].value(), form['email'].value(), form['profile_summary'].value(),
                            form['skills'].value(), form['tools'].value()):
                personal.complete_status = True
            with transaction.atomic():
                self.object = form.save(commit=False)
                if languages.is_valid():
                    languages.instance = self.object
                    languages.parent_user = self.request.user
                    languages.save()
            return super(UpdateResumePersonalView, self).form_valid(form)


update_personal_resume_form = UpdateResumePersonalView.as_view()


class ManageResumeExperience(LoginRequiredMixin, ModelFormSetView):
    model = Experience
    template_name = 'resume/resume_form_experience.html'
    form_class = ManageExperience # CreateExperience
    success_url = '/resume/educations/'
    factory_kwargs = {'extra': 0, 'max_num': 5, 'min_num': 1, 'validate_min': True,  'can_delete': True}

    def get_context_data(self, **kwargs):
        context = super(ManageResumeExperience, self).get_context_data(**kwargs)
        if self.request.POST:
            context['experiences'] = ExperienceFormSet(self.request.POST)
        else:
            context['experiences'] = ExperienceFormSet
        return context

    def get_queryset(self):
        # company_permission = Permission.objects.get(name='Can add companies')
        # position_permission = Permission.objects.get(name='Can add positions')
        user = self.request.user
        # user.user_permissions.add(company_permission)
        # user.user_permissions.add(position_permission)
        data = super(ManageResumeExperience, self).get_queryset().filter(candidate=user)
        return data

    def formset_valid(self, formset):
        print('submitted')
        for form in formset:
            if form.is_valid():
                resume = form.save(commit=False)
                resume.candidate = self.request.user
                date_today = date.today().strftime('%Y-%m-%d')
                if None not in (form['position'].value(), form['company'].value(), form['location'].value(),
                                form['work_start_date'].value(), form['work_end_date'].value(), form['industry'].value(),
                                form['subindustry'].value(), form['position_description'].value(),
                                form['selected_accomplishment_1'].value(), form['selected_accomplishment_2'].value(),
                                form['selected_accomplishment_3'].value()):
                    resume.complete_status = True
                if form['work_end_date'].value() == date_today or form['work_end_date'].value() == "":
                    resume.currently_working_here = True
                else:
                    resume.currently_working_here = False
                company = form['company'].value()
                Companies.objects.create_company(name=company)
                resume.save()
        return super(ManageResumeExperience, self).formset_valid(formset)


experience_resume_form = ManageResumeExperience.as_view()


class ManageResumeEducation(LoginRequiredMixin, ModelFormSetView):
    model = Education
    template_name = 'resume/resume_form_education.html'
    form_class = ManageEducation
    success_url = '/resume/references/'
    factory_kwargs = {'extra': 0, 'max_num': 5, 'min_num': 1, 'validate_min': True,  'can_delete': True}

    def get_context_data(self, **kwargs):
        context = super(ManageResumeEducation, self).get_context_data(**kwargs)
        if self.request.POST:
            context['educations'] = EducationFormSet(self.request.POST)
        else:
            context['educations'] = EducationFormSet
        return context

    def get_queryset(self):
        education_permission = Permission.objects.get(name='Can add education')
        user = self.request.user
        user.user_permissions.add(education_permission)
        data = super(ManageResumeEducation, self).get_queryset().filter(candidate=user)
        return data

    def formset_valid(self, formset):
        print('submitted')
        for form in formset:
            if form.is_valid():
                resume = form.save(commit=False)
                resume.candidate = self.request.user
                if None not in (form['institution'].value(), form['degree'].value(), form['education_start_date'].value(),
                                form['education_end_date'].value()):
                    resume.complete_status = True
                resume.save()
        return super(ManageResumeEducation, self).formset_valid(formset)


education_resume_form = ManageResumeEducation.as_view()


class ManageResumeReference(LoginRequiredMixin, ModelFormSetView):
    model = Reference
    template_name = 'resume/resume_form_reference.html'
    form_class = CreateReference
    success_url = '/dashboard/'
    factory_kwargs = {'extra': 0, 'max_num': 5, 'min_num': 1, 'validate_min': True,  'can_delete': True}

    def get_context_data(self, **kwargs):
        context = super(ManageResumeReference, self).get_context_data(**kwargs)
        if self.request.POST:
            context['references'] = EducationFormSet(self.request.POST)
        else:
            context['references'] = EducationFormSet
        return context

    def get_queryset(self):
        position_permission = Permission.objects.get(name='Can add positions')
        user = self.request.user
        user.user_permissions.add(position_permission)
        data = super(ManageResumeReference, self).get_queryset().filter(candidate=user)
        return data

    def formset_valid(self, formset):
        print('submitted')
        for form in formset:
            if form.is_valid():
                resume = form.save(commit=False)
                resume.candidate = self.request.user
                if None not in (form['first_name'].value(), form['last_name'].value(), form['current_position'].value(),
                                form['phone'].value(), form['email'].value()):
                    resume.complete_status = True
                resume.save()
        return super(ManageResumeReference, self).formset_valid(formset)


reference_resume_form = ManageResumeReference.as_view()


class ResumeExperienceListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    serializer_class = ResumeExperienceSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        candidate = self.kwargs['candidate']
        return Experience.objects.filter(candidate=candidate)


resume_experience_list_api = ResumeExperienceListAPIView.as_view()


class ResumeEducationListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    serializer_class = ResumeEducationSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        candidate = self.kwargs['candidate']
        return Education.objects.filter(candidate=candidate)


resume_education_list_api = ResumeEducationListAPIView.as_view()


class ResumeReferenceListAPIView(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)

    serializer_class = ResumeReferenceSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        candidate = self.kwargs['candidate']
        return Reference.objects.filter(candidate=candidate)


resume_reference_list_api = ResumeReferenceListAPIView.as_view()


class ResumePersonalDetailAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    queryset = Personal.objects.all()
    serializer_class = ResumePersonalSerializer
    lookup_field = 'parent_user'


resume_personal_detail_api = ResumePersonalDetailAPIView.as_view()


class CreateTailoredResumePDFExperienceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    queryset = TailoredResumePDFExperience.objects.all()
    serializer_class = TailoredResumePDFExperienceSerializer


create_tailored_pdf_resume_experience = CreateTailoredResumePDFExperienceViewSet.as_view({'post': 'create'})


class CreateTailoredResumePDFEducationViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    queryset = TailoredResumePDFEducation.objects.all()
    serializer_class = TailoredResumePDFEducationSerializer


create_tailored_pdf_resume_education = CreateTailoredResumePDFEducationViewSet.as_view({'post': 'create'})


class CreateTailoredResumePDFPersonalViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    queryset = TailoredResumePDFPersonal.objects.all()
    serializer_class = TailoredResumePDFPersonalSerializer


create_tailored_pdf_resume_personal = CreateTailoredResumePDFPersonalViewSet.as_view({'post': 'create'})


class CreateTailoredResumePDFReferenceViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    queryset = TailoredResumePDFReference.objects.all()
    serializer_class = TailoredResumePDFReferenceSerializer


create_tailored_pdf_resume_reference = CreateTailoredResumePDFReferenceViewSet.as_view({'post': 'create'})
