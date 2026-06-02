# resume/urls.py
# from django.conf.urls import url
# from rest_framework.authtoken.views import obtain_auth_token
# from django.urls import path, include
# from django.views.decorators.csrf import csrf_exempt


# from jobassistant.cover_letter_tracking.views import (
#     create_original_cover_letter,
#     original_cover_letter_detail,
#     create_basic_cover_letter,
#     create_full_cover_letter,
#     # full_cover_letter_list,
#     create_updated_full_cover_letter,
#     raw_job_title,
#     job_title,
#     raw_company,
#     company,
#     name,
#     raw_name,
# )


# app_name = 'cover_letter_tracking'

#
# urlpatterns = [
#     url(r'create-original-cover-letter/$',
#         create_original_cover_letter,
#         name='api-create-original-cover-letter',
#         ),
#     url(r'original-cover-letter-detail/(?P<pk>\d+)/$',
#         original_cover_letter_detail,
#         name='api-original-cover-tracking-detail',
#         ),
#     url(r'create-basic-cover-letter/$',
#         create_basic_cover_letter,
#         name='api-create-basic-cover-letter',
#         ),
#     url(r'create-full-cover-letter/$',
#         create_full_cover_letter,
#         name='api-create-full-cover-letter',
#         ),
#     # url(r'full-cover-letter-list/(?P<sender>.+)/$',
#     #     full_cover_letter_list,
#     #     name='api-full-cover-letter-list',
#     #     ),
#     url(r'create-updated-full-cover-letter/$',
#         create_updated_full_cover_letter,
#         name='api-create-updated-cover',
#         ),
#     url(r'raw_job_title/$',
#         raw_job_title,
#         name='raw_job_title',
#         ),
#     url(r'job_title/(?P<job_title>.+)/$',
#         job_title,
#         name='job_title',
#         ),
#     url(r'contact-name/(?P<name>.+)/$',
#         name,
#         name='name',
#         ),
#     url(r'raw-contact-name/$',
#         raw_name,
#         name='raw-name',
#         ),
#     url(r'raw_company/$',
#         raw_company,
#         name='raw_company',
#         ),
#     url(r'company/(?P<company>.+)/$',
#         company,
#         name='company',
#         ),
#     path('api-token-auth/',
#          csrf_exempt(obtain_auth_token),
#          name='api_token_auth',
#          ),
# ]
