from rest_framework import serializers
from .models import Account, Project

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ("user", "account_image", "bio", "contact")

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ("user", "title", "descr", "image", "url", "location", "date")
