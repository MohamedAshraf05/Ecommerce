from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name' , 'email' , 'password' , 'id']
        extra_kwargs = {
            'password' : {'write_only' : True} 
        } # to hide the password from the response
    
    
    # to hashing the password 
    def create(self, validated_data):
        password = validated_data.pop('password' , None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

