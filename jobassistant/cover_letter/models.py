# Model related imports
import uuid
from django.db import models
from django.urls import reverse

# User model
from django.conf import settings

# Third party imports


User = settings.AUTH_USER_MODEL


class CoverLetterManager(models.Manager):

    def create_cover_letter(self, parent_user, text, form_id, job, contact, industry, company, cover_letter_pdf_url, resume_pdf_url):
        cover_letter = self.create(parent_user=parent_user, text=text, form_id=form_id, job=job, contact=contact,
                                   industry=industry, company=company, cover_letter_pdf_url=cover_letter_pdf_url,
                                   resume_pdf_url=resume_pdf_url)
        return cover_letter

    def get_coverletter(self, user):
        return self.filter(parent_user=user)

    def get_coverletter_from_form_id(self, form_id):
        return self.filter(form_id=form_id)

    class Meta:
        managed = True
        app_label = 'cover_letter'


class CoverLetter(models.Model):
    objects = CoverLetterManager()
    id = models.AutoField(primary_key=True)
    parent_user = models.ForeignKey(User,
                                    null=True,
                                    on_delete=models.CASCADE,
                                    blank=False)
    company = models.CharField(max_length=150, null=True, blank=True)
    job = models.CharField(max_length=150, null=True, blank=True)
    contact = models.CharField(max_length=150, null=True, blank=True)
    industry = models.CharField(max_length=150, null=True, blank=True)
    form_id = models.CharField(max_length=100, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    cover_letter_pdf_url = models.CharField(max_length=300, null=True, blank=True)
    resume_pdf_url = models.CharField(max_length=300, null=True, blank=True)

    STATUS_CHOICES = (
        ("", "---"),
        ("SENT TO EMPLOYER", "Sent to employer"),
        ("GOT INTERVIEW", "Got interview"),
        ("HIRED", "hired"),
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="", null=True, blank=True)
    # TODO: success_status = models.BooleanField() HIDDEN in form
    # TODO: customized_resume_url = models.CharField(max_length=300, null=True, blank=False) HIDDEN in form
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    objects = CoverLetterManager()

    class Meta:
        managed = True
        app_label = 'cover_letter'

    def get_absolute_url(self):
        return reverse('cover_letter:update-cover-letter', kwargs={'pk': self.pk})

    def __str__(self):
        form_id = str(self.form_id)
        return form_id

