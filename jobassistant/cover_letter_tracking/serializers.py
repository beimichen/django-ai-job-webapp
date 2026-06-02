# from rest_framework import serializers
# from .models import *
# from django.conf import settings
#
#
# User = settings.AUTH_USER_MODEL
#
#
# class OriginalCoverLetterSerializer(serializers.ModelSerializer):
#     # TODO: consider hyperlinks for maintainability and flexibility https://reflectoring.io/rest-hypermedia/
#     # https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/
#     class Meta:
#         model = OriginalFullCoverLetter
#         fields = ('__all__')
#
#
# class BasicCoverLetterSerializer(serializers.ModelSerializer):
#     # TODO: consider hyperlinks for maintainability and flexibility https://reflectoring.io/rest-hypermedia/
#     # https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/
#     class Meta:
#         model = BasicCoverLetter
#         fields = ('__all__')
#
#
# class FullCoverLetterSerializer(serializers.ModelSerializer):
#     # TODO: consider hyperlinks for maintainability and flexibility https://reflectoring.io/rest-hypermedia/
#     # https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/
#     class Meta:
#         model = FullCoverLetter
#         fields = ('__all__')
#
#
# class UpdatedFullCoverLetterSerializer(serializers.ModelSerializer):
#     # TODO: consider hyperlinks for maintainability and flexibility https://reflectoring.io/rest-hypermedia/
#     # https://www.django-rest-framework.org/tutorial/5-relationships-and-hyperlinked-apis/
#     class Meta:
#         model = UpdatedFullCoverLetter
#         fields = ('__all__')
#
#
# class UserSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = User
#         fields = ('__all__')
#
#
# # https://www.django-rest-framework.org/api-guide/relations/
# class RawJobTitleSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = RawJobTitle
#         fields = ('__all__')
#
#
# class JobTitleSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = JobTitle
#         fields = ('__all__')
#
#
# class RawCompanySerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = RawCompany
#         fields = ('__all__')
#
#
# class CompanySerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Company
#         fields = ('__all__')
#
#
# class RawPersonNameSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = RawPersonName
#         fields = ('__all__')
#
#
# class PersonNameSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = PersonName
#         fields = ('__all__')
