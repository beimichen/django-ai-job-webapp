from django.forms import ModelForm

# Models
from .models import *


class CreateCoverLetter(ModelForm):
    class Meta:
        model = CoverLetter
        exclude = ['parent_user', 'created_at', 'updated_at', 'job', 'company', 'status', 'cover_letter_pdf_url',
                   'resume_pdf_url']

