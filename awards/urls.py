"""awards URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib import admin
from django.urls import path,include,reverse
from django.conf import settings
from django.conf.urls.static import static
# from usersaccount import views as user_views
from django.contrib.auth import views as auth_views
from django.urls import path


from allprojects import views as user_views
from allprojects import views 

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # path('',include('projects.urls')),
    # path('',include('authentic.urls')),
    path('homeview', views.home, name='homeview'),
    path('register/', user_views.register, name='register'),
    path('home/', views.home, name='home'),
    path('profileacc/',views.profile, name='profileacc'),
   
#    using  LoginView and LogoutView, class based views, they have the logic but we show them how to handle templates
    # path('login',auth_views.LoginView.as_view(template_name='neighapp/login.html'),name='login'),
    # path('logout',auth_views.LogoutView.as_view(template_name='neighapp/logout.html'),name='logout'),

    
    # path('',user_views.home,name='home'),
    path('login/',auth_views.LoginView.as_view(template_name='usersaccount/login.html'),name='login'),
    # path('register/',user_views.register,name='register'),
    # path('profile/',user_views.profile,name='profile'),
    path('logout/',auth_views.LogoutView.as_view(template_name='usersaccount/logout.html'),name='logout'),
    
    
    path('',include('allprojects.urls'))
    
]


    
    
