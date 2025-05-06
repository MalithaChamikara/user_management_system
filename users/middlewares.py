from rest_framework.exceptions import AuthenticationFailed ## used to raise an error if token is invalid or expired
from .auth import verify_token
import re
from django.conf import settings

## class that manually handles JWT-based authentication for incoming http requests
class JWTAuthenticationMiddleware:
    def __init__(self,get_response):
        self.get_response = get_response ##sends the request to the next middleware/view
    

    ## Looks  for the authorization headers in the request
    def __call__(self,request):
        

        # Check if the current path is exempt from JWT authentication
        if any(re.match(m, request.path) for m in settings.JWT_EXEMPT_PATHS):
            return self.get_response(request)
        
        auth_header = request.headers.get('Authorization')

        ## token extraction
        if auth_header and  auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

        ## decode the token for gets the payload
        payload = verify_token(token)

        if payload:
            request.user_id = payload['user_id']
        else:
            raise AuthenticationFailed('Invalid or expired Token')

        return self.get_response(request)
