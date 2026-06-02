from jobassistant.resume.models import *


def personal_check_complete(request):
    if request.user.is_authenticated:
        try:
            personal_id = list(Personal.objects.get_personal(request.user).values("id"))
            if personal_id == []:
                dict = {}
                return dict
            else:
                personal_resume = True
                dict = {"personal": personal_resume, "personal_id": personal_id[0]['id']}
                return dict
        except Personal.DoesNotExist:
            return {}
    else:
        return{}


def experience_check_complete(request):
    if request.user.is_authenticated:
        try:
            experience = list(Experience.objects.get_experience(request.user).values())
            print(experience)
            if experience == []:
                return {}
            else:
                experience = True
                return {"experience": experience}
        except Experience.DoesNotExist:
            return {}
    else:
        return{}


def education_check_complete(request):
    if request.user.is_authenticated:
        try:
            education = list(Education.objects.get_education(request.user).values())
            print(education)
            if education == []:
                return {}
            else:
                education = True
                return {"education": education}
        except Education.DoesNotExist:
            return {}
    else:
        return{}


def reference_check_complete(request):
    if request.user.is_authenticated:
        try:
            reference = list(Reference.objects.get_reference(request.user).values())
            print(reference)
            if reference == []:
                return {}
            else:
                reference = True
                return {"reference": reference}
        except Reference.DoesNotExist:
            return {}
    else:
        return{}

