from django.conf import settings
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.conf.urls import url

urlpatterns = [
    # Root
    path(
        "",
        TemplateView.as_view(template_name="pages/home.html"),
        name="home"
    ),
    # Chat app
    path(
        "chat/",
        include("jobassistant.chat.urls",
                namespace="chat"),
    ),
    # Taggit Selectize
    path(
        'taggit/',
        include('taggit_selectize.urls'),
    ),
    # Resume app
    path(
        "resume/",
        include("jobassistant.resume.urls",
                namespace="resume"),
    ),
    # Cover letter
    path(
        "cover-letter/",
        include("jobassistant.cover_letter.urls",
                namespace="cover_letter"),
    ),
    # Cover letter API
    # path(
    #     "cover-letter-api/",
    #     include("jobassistant.cover_letter_tracking.urls",
    #             namespace="cover-letter-api")
    # ),
    # Dashboard
    path(
        "dashboard/",
        include("jobassistant.dashboard.urls",
                namespace="dashboard"),
    ),
    # Static page
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(
        settings.ADMIN_URL,
        admin.site.urls),
    # User management
    path(
        "users/",
        include("jobassistant.users.urls",
                namespace="users"),
    ),
    path(
        "accounts/",
         include("allauth.urls")
    ),
    # smart_selects
    path(
        'chaining/',
        include('smart_selects.urls')
    ),
    path('contact/',
         include('jobassistant.contact.urls')
         )
    # google_analytics
    # url(
    #     r'^djga/',
    #     include('google_analytics.urls')
    # ),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
