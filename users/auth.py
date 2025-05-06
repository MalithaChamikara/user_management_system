import jwt ## JWT library used to encode/decode JSON web tokens
from datetime import datetime,timedelta ## To handle token expiration times
from decouple import config ## Library to load environemnt variables securely
from django.contrib.auth.hashers import check_password ## built in password matcher
from .models import UserDetails

## function to generate token only for authenticated users
def generate_token(user):
    ## define payload required to generate a token
    payload = {
        "user_id":user.UserID, ## unique identifier
        "email":user.Email,
        "exp":datetime.utcnow() + timedelta(hours=2), ## token expiration
        "iat":datetime.utcnow() ## issued at time
    }
    ## create and return token
    token = jwt.encode(payload,config('JWT_SECRET_KEY'),algorithm='HS256') ## encoding the payload
    return token

## Function to verify token
def verify_token(token):
    ## Extract payload data from the token if token is valid
    try:
        payload = jwt.decode(token,config('JWT_SECRET_KEY'),algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None ## Token is expired
    except jwt.InvalidTokenError:
        return None ## Token is invalid


## Function to login users 
def login_user(email,password):
    try:
        user = UserDetails.objects.get(Email = email) ## find user by email
        ## check password are matching
        if check_password(password,user.Password):
            return user
        return None ## If password is wrong
    except UserDetails.DoesNotExist:
        return None ## If user does not exists


