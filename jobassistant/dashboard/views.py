from django.shortcuts import render, get_object_or_404
from django.utils.safestring import mark_safe
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.decorators import login_required

from tools import *
from jobassistant.cover_letter.models import *
from jobassistant.resume.models import *

from .pdf_generation_resume import default_template_resume_pdf
import json
import requests


@login_required
def dashboard_menu(request):
    personal = list(Personal.objects.get_personal(request.user.id).values())
    print(personal)

    return JsonResponse({'personal': personal})


dashboard_menu = dashboard_menu


@ensure_csrf_cookie
def dashboard(request):
    user_id = str(request.user.id)

    env_url, admin, password, bucket = check_environment('dashboard')

    urls = get_resume_api_endpoints(env_url, user_id)

    headers = get_token(admin, password, env_url)

    generate_resume = request.POST.get('generate_resume')
    status = request.POST.get('status')
    delete_job_app = request.POST.get('delete_job_app')

    cover_letters = CoverLetter.objects.get_coverletter(request.user.id)
    cover_letters = cover_letters.values()
    cover_letters = [cover_letter for cover_letter in cover_letters]

    try:
        personal_info = requests.get(urls['resume_personal_url'], headers=headers)
        personal_info = personal_info.text
        personal_info = json.loads(personal_info)
    except Exception as e:
        print(e)
        print(e.args)
        personal_info = ''

    form_ids = []

    for cover_letter in cover_letters:
        form_ids.append(cover_letter['form_id'])

    print(form_ids)

    if delete_job_app:
        json.loads(delete_job_app)
        form_id = json.loads(delete_job_app)
        print("TEST FORM ID")
        print(form_id)
        CoverLetter.objects.get(form_id=form_id).delete()
        TailoredResumePDFExperience.objects.get_tailored_experience(form_id).delete()

    for _id in form_ids:
        resume_experiences = TailoredResumePDFExperience.objects.get_tailored_experience(_id)
        resume_experiences = resume_experiences.values()
        resume_experiences = [experience for experience in resume_experiences]
        resume_educations = TailoredResumePDFEducation.objects.get_tailored_education(_id)
        resume_educations = resume_educations.values()
        resume_educations = [education for education in resume_educations]
        resume_references = TailoredResumePDFReference.objects.get_tailored_reference(_id)
        resume_references = resume_references.values()
        resume_references = [reference for reference in resume_references]
        for cover_letter in cover_letters:
            # print(cover_letter['status'])
            if cover_letter['form_id'] is _id and resume_experiences is not None:
                cover_letter['experiences'] = resume_experiences
                cover_letter['educations'] = resume_educations
                cover_letter['references'] = resume_references
            elif cover_letter['form_id'] is _id and resume_experiences is None:
                cover_letter['experiences'] = None
                cover_letter['educations'] = None
                cover_letter['references'] = None

    # print(cover_letters)
    skills = ""
    tools = ""
    if personal_info != '':
        try:
            if personal_info['skills_tags']:
                skills = personal_info['skills_tags']
                tools = personal_info['tools_tags']
                # print(skills)
        except:
            skills = ""
            tools = ""
            # print("Skills: None")

    if status:
        cover_letter_status = json.loads(status)
        form_id = cover_letter_status['form_id']
        # print(form_id)
        if cover_letter_status['status'] == "Generated cover letter":
            CoverLetter.objects.filter(form_id=form_id).update(status="")
        elif cover_letter_status['status'] == "Sent the cover letter":
            CoverLetter.objects.filter(form_id=form_id).update(status="SENT TO EMPLOYER")
        elif cover_letter_status['status'] == "Got Interview":
            CoverLetter.objects.filter(form_id=form_id).update(status="GOT INTERVIEW")
        elif cover_letter_status['status'] == "Hired!":
            CoverLetter.objects.filter(form_id=form_id).update(status="HIRED")

    if generate_resume:
        print('success!')
        form = json.loads(generate_resume)

        form_id = form['form_id']
        position = form['position']
        position = position.lower()
        industry = form['industry']  # Or can use s3 file

        personal_resume_data = requests.get(urls['resume_personal_url'], headers=headers)
        experience_resume_data = requests.get(urls['resume_experience_url'], headers=headers)
        education_resume_data = requests.get(urls['resume_education_url'], headers=headers)
        reference_resume_data = requests.get(urls['resume_reference_url'], headers=headers)

        personal_resume_data = json.loads(personal_resume_data.text)
        experience_resume_data = json.loads(experience_resume_data.text)
        education_resume_data = json.loads(education_resume_data.text)
        reference_resume_data = json.loads(reference_resume_data.text)

        personal_resume_data['experience'] = experience_resume_data
        personal_resume_data['education'] = education_resume_data
        personal_resume_data['referees'] = reference_resume_data

        resume_data = personal_resume_data
        resume_pdf_url = default_template_resume_pdf(env_url, admin, password, resume_data, position, industry, form_id)

        CoverLetter.objects.filter(form_id=form_id).update(resume_pdf_url=resume_pdf_url)

        return render(
            request,
            'dashboard/dashboard_main.html',
            {
                "response": "success"
            }
        )

    return render(
        request,
        'dashboard/dashboard_main.html',
        {
            "cover_letters": cover_letters,
            "user": personal_info,
            "skills": skills,
            "tools": tools,
        }
    )


dashboard_main_view = dashboard
