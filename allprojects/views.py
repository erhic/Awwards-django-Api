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
from authentic import views

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile

# def home(request):
#     return render(request,'authentic/base.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
@login_required()
def profile(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('home')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'authentic/profile.html', context)

def home(request): 
    project = Project.objects.all()
    # latest_project = project[0]
  
    return render(
        request, "landing.html", {"projects": project}
    )

def project_info(request, project_id):
    project = Project.objects.get(id=project_id)
   
    return render(request, "projectupload.html", {"project": project, })


@login_required
def account(request): 
    current_user = request.user
    account = Account.objects.filter(user_id=current_user.id).first()  
    project = Project.objects.filter(user_id=current_user.id).all()  
    return render(request, "profile.html", {"account": account, "images": project})


@login_required
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
        return redirect( 'home')
       
    
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
