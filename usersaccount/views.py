
from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegisterForm
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
# from django.urls import reverse, reverse_lazy

def home (request):
    return render (request, 'landing.html')

def register (request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created successfuly')
            return redirect ('posts:postlist')
            # success_url = reverse_lazy("posts:postlist")
    else:
        form=UserRegisterForm()
        
    return render (request, 'landing.html',{'form':form})

@login_required
def profile(request):
    return render (request,'usersaccount/profile.html')