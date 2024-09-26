import jwt
from users.models import User
from rest_framework.exceptions import AuthenticationFailed

def AuthenticateUser(request):
    # Retrieve JWT token from cookies
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed("Unauthenticated!!")

    # Validate the token
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token has expired")
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Invalid token")
    except Exception as e:
        raise AuthenticationFailed(f"Unauthenticated: {str(e)}")

    # Fetch the user if the token is valid
    user = User.objects.filter(id=payload['id']).first()
    if not user:
        raise AuthenticationFailed("User not found")

    return user
