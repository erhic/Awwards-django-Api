from rest_framework import serializers
from authentication.models import User


class RegisterSerializer(serializers.ModelSerializer):
    
    password= serializers.CharField(write_only=True,max_length=70)
    
    
    class Meta:
        model= User
        fields= ('username','email','password')
        
        
        def create(self,validated_data):
            return User.objects.create_user(**validated_data)