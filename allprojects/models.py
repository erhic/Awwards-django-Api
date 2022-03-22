from django.db import models

# Create your models here.
import datetime as dt
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from allprojects.models import User

from django.db import models

# .............

from  PIL import Image



class Profile(models.Model):
    user= models.OneToOneField(User, on_delete=models.CASCADE)
    image= CloudinaryField("image",default='default.png',)
    contact=models.CharField(blank=True,max_length=50)
    
    def __str__(self):
        return f'{self.user.username}Profile'
    
    
    def save(self,**kwarg):
        super().save()
        #  the below variable will store  every instance of the image before risizing
        img= Image.open(self.image.path)
        
        if img.height>300 or img.width>300:
            output_size=(300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)
        


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    description = models.TextField()
    image = CloudinaryField("image",default='default.png')
    url = models.URLField(blank=True)
    location = models.CharField(max_length=100, )
    date = models.DateTimeField(auto_now_add=True, null=True)

    @classmethod
    def search_by_title(cls, search_term):
        projects = cls.objects.filter(title__icontains=search_term)
        return projects

    @classmethod
    def get_project_by_id(cls, id):
        project = cls.objects.get(id=id)
        return project

    @classmethod
    def get_all_projects(cls):
        projects = cls.objects.all()
        return projects

    @classmethod
    def get_all_projects_by_user(cls, user):
        projects = cls.objects.filter(user=user)
        return projects


    def save_project(self):
        self.save()

    def delete_project(self):
        self.delete()
  
    def update_project(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        self.save()

    def __str__(self):
        return self.title

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_image = CloudinaryField("image",default='default.png')
    bio = models.TextField(max_length=250, blank=True, null=True)
    contact = models.CharField(max_length=250, blank=True, null=True)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def filter_by_id(cls, id):
        profile = Account.objects.filter(user=id).first()
        return profile

    def __str__(self):
        return self.user.username

class ProjectRate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    content_rate = models.IntegerField(default=0, blank=True, null=True)
    design_rate = models.IntegerField( null=True, default=0, blank=True)
    usability_rate = models.IntegerField(blank=True,default=0,  null=True)
    avg_rate = models.IntegerField( blank=True,default=0, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def save_rating(self):
        self.save()

    def delete_rating(self):
        self.delete()

    @classmethod
    def filter_by_id(cls, id):
        rating =  ProjectRate.objects.filter(id=id).first()
        return rating

    def __str__(self):
        return self.user.usernames