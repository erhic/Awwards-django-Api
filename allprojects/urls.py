# from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("account/", views.account, name="account"),
    path("profile/account/", views.account, name="account"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("project/upload/", views.upload_project, name="upload_project"),
    path("search/", views.search_project, name="search_project"),
    path("project/<int:project_id>/", views.project_info, name="project_info"),
    
   

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)