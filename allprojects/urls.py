# from django.conf.urls import url
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from allprojects import views as user_views
from allprojects import views 

from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.home, name="home"),
    path("account/", views.account, name="account"),
    path("profile/account/", views.account, name="account"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("project/upload/", views.upload_project, name="upload_project"),
    path("search/", views.search_project, name="search_project"),
    path("project/<int:project_id>/", views.project_info, name="project_info"),
    
    path('homeview', views.home, name='homeview'),
    path('register/', user_views.register, name='register'),
    path('home/', views.home, name='home'),
    path('profileacc/',views.profile, name='profileacc'),
   
#    using  LoginView and LogoutView, class based views, they have the logic but we show them how to handle templates
    path('login',auth_views.LoginView.as_view(template_name='login.html'),name='login'),
    path('logout',auth_views.LogoutView.as_view(template_name='logout.html'),name='logout'),

   

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)