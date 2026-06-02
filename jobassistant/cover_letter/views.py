# Django components
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from jobassistant.cover_letter.models import *
from jobassistant.resume.models import Personal
from tools import *
from jobassistant.cover_letter.recreate_cover_letter_pdf import pdf_cover_letter_edit_from_dashboard
import json



class CoverLetterList(ListView):
    model = CoverLetter
    template_name = 'cover_letter/cover_letter_list.html'

    def get_queryset(self, *args, **kwargs):
        # id = self.request.user.id
        # test = CoverLetter.objects.all().filter(parent_user__exact=id).values()
        # print(test)
        return CoverLetter.objects.all().filter(parent_user=self.request.user)


cover_letter_list = CoverLetterList.as_view()


class CreateCoverLetterView(LoginRequiredMixin, CreateView):
    model = CoverLetter
    fields = ['text']
    exclude = ['parent_user', 'form_id', 'created_at', 'updated_at', 'job', 'company', 'industry', 'contact', 'status',
               'cover_letter_pdf_url', 'resume_pdf_url']
    template_name = 'cover_letter/cover_letter.html'
    success_url = reverse_lazy('cover_letter:cover-letter-list')

    def form_valid(self, form):
        # uuid_instance = uuid.uuid4()
        if form.is_valid():
            form.save(commit=False)
            with transaction.atomic(using='default'):
                # populate fields with API cover letter data here
                form.parent_user = self.request.user
                # form.form_id = uuid_instance
                form.save()
            # with transaction.atomic(using='chatdb'):
            # OriginalCoverLetter.objects.create(parent_user=self.request.user.username, form_id=uuid_instance,
            # candidate_name=candidate_name, company=company,
            # body=body, selected_accomplishment_preline= selected_accomplishment_preline,
            # selected_accomplishments=selected_accomplishments, sign_off=sign_off)
            return super(CreateCoverLetterView, self).form_valid(form)


# create_cover_letter = CreateCoverLetterView.as_view() # TODO: make this unavailable- no url and no view for create


class UpdateCoverLetterView(LoginRequiredMixin, UpdateView):
    model = CoverLetter
    fields = ['text', 'form_id', 'company', 'contact', 'job']
    exclude = ['parent_user', 'created_at', 'updated_at', 'industry', 'status', 'cover_letter_pdf_url',
               'resume_pdf_url']
    template_name = 'cover_letter/cover_letter.html'
    success_url = reverse_lazy('dashboard:dashboard')

    def form_valid(self, form):
        if form.is_valid():
            env_url, admin, password, bucket = check_environment('chat')

            cover_letter_form = form.save(commit=False)
            form.parent_user = self.request.user
            personal_model_data = Personal.objects.get_personal(form.parent_user)
            print('test')
            print(personal_model_data.exists())

            if personal_model_data.exists():
                first_name = personal_model_data.values('first_name')[0]['first_name']
                user_second_name = personal_model_data.values('middle_name')[0]['middle_name']
                user_third_name = personal_model_data.values('last_name')[0]['last_name']
            else:
                first_name = ""
                user_second_name = ""
                user_third_name = ""

            form_id = form['form_id'].value()
            sender_id = form_id

            file_name = sender_id + '.json'
            s3_file = bucket.Object(file_name)
            chat_obj = json.loads(fetch_data_from_s3_file(s3_file))

            text = form['text'].value()
            company = form['company'].value()
            contact = form['contact'].value()
            position = form['job'].value()
            updated_cover_letter_url = pdf_cover_letter_edit_from_dashboard(env_url, form_id, text, first_name, user_second_name, user_third_name,
                                                       company, contact, position)

            cover_letter_form.cover_letter_pdf_url = updated_cover_letter_url

            cover_letter_form.save()
            chat_obj['slots']['edited_cover_letter'] = text
            data = chat_obj
            data_type = 'chat'
            file_name = form_id + '.json'
            store_data_s3(data, data_type, sender_id, file_name, env_url)  # data, data_type, sender_id, file_name, env_url

            return super(UpdateCoverLetterView, self).form_valid(form)


update_cover_letter = UpdateCoverLetterView.as_view()
