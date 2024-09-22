import datetime , jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from .serializers import UserSerializer
from .models import User
from rest_framework.response import Response
# Create your views here.

"""
What RegisterView need :
1. A Post Method to post these data:
    a. first get the email
    b. second get the password
    c. serialize these data 
    d. save it
    e. return the response 
"""


class RegisterView(APIView):
    def post(self , request):
        serializers = UserSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors)
        

"""
LoginView requirments:
1. A Post Method to post these data:
    a. email
    b. password
    c. find the user who matches these data
    d. return the response
"""

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
        token = request.COOKIES.get('jwt')

        if not token:
            print("I couldn't get the token")
            raise AuthenticationFailed("Unauthenticated!!")
        
        print(f"this is the token : {token}")
        
        try:
            # Corrected algorithms to be plural
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            print("Token has expired")
            raise AuthenticationFailed("Token has expired")
        except jwt.InvalidTokenError:
            print("Invalid token")
            raise AuthenticationFailed("Invalid token")
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise AuthenticationFailed("Unauthenticated!!")


        print("token is valid")    
        # Fetch the user if the token is valid
        user = User.objects.filter(id=payload['id']).first()
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