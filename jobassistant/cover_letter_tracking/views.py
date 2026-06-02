# Third party
# from rest_framework import viewsets

# Serializer and model
# from jobassistant.cover_letter_tracking.serializers import *
# from jobassistant.cover_letter_tracking.models import *
# from jobassistant.cover_letter.models import CoverLetter

# rest framework
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import generics
# from django_filters.rest_framework import DjangoFilterBackend

# from rest_framework.authentication import SessionAuthentication, BasicAuthentication

#
# class OriginalCoverLetterViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#
#     queryset = OriginalFullCoverLetter.objects.all()
#     serializer_class = OriginalCoverLetterSerializer
#
#
# create_original_cover_letter = OriginalCoverLetterViewSet.as_view({'post': 'create'})
#
# original_cover_letter_detail = OriginalCoverLetterViewSet.as_view({'get': 'retrieve',
#                                                            'put': 'update',
#                                                            'patch': 'partial_update',
#                                                            'delete': 'destroy'})
#
#
# class CreateBasicCoverLetterViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#
#     queryset = BasicCoverLetter.objects.all()
#     serializer_class = BasicCoverLetterSerializer
#
#
# create_basic_cover_letter = CreateBasicCoverLetterViewSet.as_view({'post': 'create'})
#
#
# # class FullCoverLetterViewSet(generics.ListAPIView):
# #     permission_classes = (IsAuthenticated,)
# #     authentication_classes = (TokenAuthentication,)
# #
# #     serializer_class = FullCoverLetterSerializer
# #
# #     def get_queryset(self):
# #         sender = self.kwargs['sender']
# #         return FullCoverLetter.objects.filter(sender=sender)
# #
# #
# # full_cover_letter_list = FullCoverLetterViewSet.as_view()
#
#
# class CreateFullCoverLetterViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#
#     queryset = FullCoverLetter.objects.all()
#     serializer_class = FullCoverLetterSerializer
#
#
# create_full_cover_letter = CreateFullCoverLetterViewSet.as_view({'post': 'create'})
#
#
# class CreateUpdatedFullCoverLetterViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#
#     queryset = UpdatedFullCoverLetter.objects.all()
#     serializer_class = UpdatedFullCoverLetterSerializer
#
#
# create_updated_full_cover_letter = CreateUpdatedFullCoverLetterViewSet.as_view({'post': 'create'})
#
#
# class RawJobTitleViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#
#     queryset = RawJobTitle.objects.all()
#     serializer_class = RawJobTitleSerializer
#
#     lookup_field = 'raw_job_title'
#
#
# raw_job_title = RawJobTitleViewSet.as_view({'post': 'create'})
#
#
# class JobTitleViewSet(generics.ListAPIView):
#     # permission_classes = (IsAuthenticated,)
#     # authentication_classes = (TokenAuthentication,)
#
#     serializer_class = JobTitleSerializer
#
#     def get_queryset(self):
#         job_title = self.kwargs['job_title']
#         return JobTitle.objects.filter(job_title=job_title)
#
#
# job_title = JobTitleViewSet.as_view()
#
#
# class RawCompanyViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#
#     queryset = RawCompany.objects.all()
#     serializer_class = RawCompanySerializer
#
#     lookup_field = 'raw_company'
#
#
# raw_company = RawCompanyViewSet.as_view({'post': 'create'})
#
#
# class CompanyViewSet(generics.ListAPIView):
#     # permission_classes = (IsAuthenticated,)
#     # authentication_classes = (TokenAuthentication,)
#
#     serializer_class = CompanySerializer
#
#     def get_queryset(self):
#         company = self.kwargs['company']
#         return Company.objects.filter(company=company)
#
#
# company = CompanyViewSet.as_view()
#
#
# class RawPersonNameViewSet(viewsets.ModelViewSet):
#     permission_classes = (IsAuthenticated,)
#     authentication_classes = (TokenAuthentication,)
#
#     queryset = RawPersonName.objects.all()
#     serializer_class = RawPersonNameSerializer
#
#     lookup_field = 'name'
#
#
# raw_name = RawPersonNameViewSet.as_view({'post': 'create'})
#
#
# class PersonNameViewSet(generics.ListAPIView):
#     # permission_classes = (IsAuthenticated,)
#     # authentication_classes = (TokenAuthentication,)
#
#     serializer_class = PersonNameSerializer
#
#     def get_queryset(self):
#         name = self.kwargs['name']
#         return PersonName.objects.filter(name=name)
#
#
# name = PersonNameViewSet.as_view()
