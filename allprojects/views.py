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
    rate = ProjectRate.objects.filter(project_id=latest_project.id).first()
  
    return render(
        request, "index.html", {"projects": project, "project_home": latest_project, "rating": rate}
    )

def project_info(request, project_id):
    project = Project.objects.get(id=project_id)
    rate =  ProjectRate.objects.filter(project=project)
    return render(request, "project.html", {"project": project, "rating": rate})


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

        return redirect("/profile", {"success": "Profile Updated Successfully"})
    else:
        return render(request, "profile.html", {"danger": "Profile Update Failed"})


# save project
@login_required(login_url="/accounts/login/")
def save_project(request):
    if request.method == "POST":

        current_user = request.user

        title = request.POST["title"]
        location = request.POST["location"]
        descr = request.POST["descr"]
        url = request.POST["url"]
        image = request.FILES["image"]
        # crop image to square
        image = cloudinary.uploader.upload(image, crop="limit", width=500, height=500)
        # image = cloudinary.uploader.upload(image)
        image_url = image["url"]

        project = Project(
            user_id=current_user.id,
            title=title,
            location=location,
            descr=descr,
            url=url,
            image=image_url,
        )
        project.save_project()

        return redirect("/profile", {"success": "Project Saved Successfully"})
    else:
        return render(request, "profile.html", {"danger": "Project Save Failed"})


# delete project
@login_required(login_url="/accounts/login/")
def delete_project(request, id):
    project = Project.objects.get(id=id)
    project.delete_project()
    return redirect("/profile", {"success": "Project Deleted Successfully"})


# rate_project
@login_required(login_url="/accounts/login/")
def rate_project(request, id):
    if request.method == "POST":

        project = Project.objects.get(id=id)
        current_user = request.user

        design_rate=request.POST["design"]
        usability_rate=request.POST["usability"]
        content_rate=request.POST["content"]

        ProjectRate.objects.create(
            project=project,
            user=current_user,
            design_rate=design_rate,
            usability_rate=usability_rate,
            content_rate=content_rate,
            avg_rate=round((float(design_rate)+float(usability_rate)+float(content_rate))/3,2),
        )

        # get the avarage rate of the project for the three rates
        avg_rating= (int(design_rate)+int(usability_rate)+int(content_rate))/3

        # update the project with the new rate
        project.rate=avg_rating
        project.update_project()

        return render(request, "project.html", {"success": "Project Rated Successfully", "project": project, "rating": ProjectRate.objects.filter(project=project)})
    else:
        project = Project.objects.get(id=id)
        return render(request, "project.html", {"danger": "Project Rating Failed", "project": project})


# search projects
def search_project(request):
    if 'search_term' in request.GET and request.GET["search_term"]:
        search_term = request.GET.get("search_term")
        searched_projects = Project.objects.filter(title__icontains=search_term)
        message = f"Search For: {search_term}"

        return render(request, "search.html", {"message": message, "projects": searched_projects})
    else:
        message = "You haven't searched for any term"
        return render(request, "search.html", {"message": message})



# rest api ====================================
class ProfileList(APIView): # get all profiles
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_profiles = Account.objects.all()
        serializers = AccountSerializer(all_profiles, many=True)
        return Response(serializers.data)

    # def post(self, request, format=None):
    #     serializers = MerchSerializer(data=request.data)


class ProjectList(APIView): # get all projects
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_projects = Project.objects.all()
        serializers = ProjectSerializer(all_projects, many=True)
        return Response(serializers.data)
