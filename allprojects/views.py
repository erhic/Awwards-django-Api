from email import message
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from rest_framework import status
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import AccountSerializer,ProjectSerializer
from .permissions import IsAdminOrReadOnly
from .models import *  
import cloudinary
import cloudinary.uploader
import cloudinary.api

def home(request): 
    project = Project.objects.all()
    latest_project = project[0]
  
    return render(
        request, "landing.html", {"projects": project, "latest_upload": latest_project}
    )

def project_info(request, project_id):
    project = Project.objects.get(id=project_id)
    # rate =  ProjectRate.objects.filter(project=project)
    return render(request, "projectupload.html", {"project": project, })


@login_required(login_url="/accounts/login/")
def account(request): 
    current_user = request.user
    account = Account.objects.filter(user_id=current_user.id).first()  
    project = Project.objects.filter(user_id=current_user.id).all()  
    return render(request, "profile.html", {"account": account, "images": project})


@login_required(login_url="/accounts/login/")
def update_profile(request):
    if request.method == "POST":

        current_user = request.user

        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        bio = request.POST["bio"]
        contact = request.POST["contact"]

        profile_image = request.FILES["profile_pic"]
        profile_image = cloudinary.uploader.upload(profile_image)
        profile_url = profile_image["url"]

        user = User.objects.get(id=current_user.id)

        # check if user exists in profile table and if not create a new profile
        if Account.objects.filter(user_id=current_user.id).exists():

            profile = Account.objects.get(user_id=current_user.id)
            profile.account_image = profile_url
            profile.bio = bio
            profile.contact = contact
            profile.save()
        else:
            profile = Account(
                user_id=current_user.id,
                account_image=profile_url,
                bio=bio,
                contact=contact,
            )
            profile.save_profile()

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email

        user.save()

    return redirect( 'home')


@login_required()
def upload_project(request):
    
    if request.method == "POST":
       
        title = request.POST["title"]
        location = request.POST["location"]
        description = request.POST["description"]
        
        url = request.POST["url"]
        
        image = request.FILES["image"]
        image = cloudinary.uploader.upload(image, crop="limit", width=600, height=600)
        image_url = image["url"]
        
        current_user = request.user
        
        project = Project(
            user_id=current_user.id,
            title=title,
            location=location,
            description=description,
            url=url,
            image=image_url,
        )
        project.save_project()
        # message='Project uploaded successfully'
    
    return render(request, "projectupload.html")



@login_required()
def delete_project(request, id):
    project = Project.objects.get(id=id)
    project.delete_project()
    return redirect("/account")



def search_project(request):
    if 'search_term' in request.GET and request.GET["search_term"]:
        search_term = request.GET.get("search_term")
        searched_projects = Project.objects.filter(title__icontains=search_term)
    

        return render(request, "search.html", { "projects": searched_projects})
    else:
        message = "You haven't searched for any term"
        return render(request, "search.html",{'message':message})




class AccountList(APIView): 
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_profiles = Account.objects.all()
        serializers = AccountSerializer(all_profiles, many=True)
        return Response(serializers.data)


class ProjectList(APIView): 
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)
