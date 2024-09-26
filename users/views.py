# View of users application

import datetime , jwt
from products.utils import AuthenticateUser
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
from rest_framework.response import Response
# Create your views here.

class RegisterView(APIView):
    def post(self , request):
        serializers = UserSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
        
class LoginView(APIView):
    def post(self , request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        
        if password is None:
            raise AuthenticationFailed('Password is None')

        if user is None:
            raise AuthenticationFailed('User not found')
        
        if not user.check_password(password):
            print(f"your password is : {password}")
            raise AuthenticationFailed('Password is incorrect')

        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.now(datetime.timezone.utc)

        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')


        response = Response()
        response.set_cookie(key='jwt' , value=token , httponly=True)
        response.data = {
            'token' : token
        }
        return response
    

class UserView(APIView):
    def get(self, request):
        user = AuthenticateUser(request)
        if not user:
            raise AuthenticationFailed("User not found")

        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        # Delete the 'jwt' cookie
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logged out successfully'
        }
        return response