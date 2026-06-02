from .models import *
from django.conf import settings

from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)

User = settings.AUTH_USER_MODEL


class ResumeExperienceSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SlugRelatedField(slug_field='candidate', read_only=True)
    position_name = serializers.CharField(source='position', read_only=True)
    company_name = serializers.CharField(source='company', read_only=True)
    industry_name = serializers.CharField(source='industry', read_only=True)
    subindustry_name = serializers.CharField(source='subindustry', read_only=True)

    class Meta:
        model = Experience
        fields = ('id', 'candidate_name', 'position_name', 'company_name', 'work_start_date', 'work_end_date',
                  'currently_working_here', 'industry_name', 'subindustry_name', 'position_description',
                  'selected_accomplishment_1', 'selected_accomplishment_2', 'selected_accomplishment_3',
                  'complete_status')
        # lookup_field = 'candidate'


class LanguagesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Language
        fields = ("language", "level")


class ResumePersonalSerializer(serializers.ModelSerializer):
    parent_user_name = serializers.SlugRelatedField(slug_field='parent_user', read_only=True)
    skills_tags = TagListSerializerField(source='skills')
    tools_tags = TagListSerializerField(source='tools')
    languages = LanguagesSerializer(many=True, read_only=True)

    class Meta:
        model = Personal
        fields = ('id', 'parent_user_name', 'first_name', 'middle_name', 'last_name', 'address', 'city', 'state', 'zip_code',
                  'country', 'phone', 'email', 'profile_summary', 'skills_tags', 'tools_tags', 'complete_status', 'languages')


class ResumeEducationSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SlugRelatedField(slug_field='candidate', read_only=True)
    institution_name = serializers.CharField(source='institution', read_only=True)

    class Meta:
        model = Education
        fields = ('id', 'institution_name', 'candidate_name', 'degree', 'education_start_date', 'education_end_date', 'complete_status')


class ResumeReferenceSerializer(serializers.ModelSerializer):
    candidate_name = serializers.SlugRelatedField(slug_field='candidate', read_only=True)
    current_position_name = serializers.CharField(source='current_position', read_only=True)

    class Meta:
        model = Reference
        fields = ('id', 'candidate_name', 'first_name', 'last_name', 'current_position_name', 'phone', 'email', 'complete_status')


class TailoredResumePDFExperienceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TailoredResumePDFExperience
        fields = ('__all__')


class TailoredResumePDFEducationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TailoredResumePDFEducation
        fields = ('__all__')


class TailoredResumePDFPersonalSerializer(serializers.ModelSerializer):

    class Meta:
        model = TailoredResumePDFPersonal
        fields = ('__all__')


class TailoredResumePDFReferenceSerializer(serializers.ModelSerializer):

    class Meta:
        model = TailoredResumePDFReference
        fields = ('__all__')
