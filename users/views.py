from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import UserDetails,RoleType,Status
from .serializers import UserDetailsSerializer, RoleTypeSerializer, StatusSerializer,LoginSerializer
from .auth import login_user,generate_token


# Create your views here.
@api_view(['GET','POST']) ## This decorator specifies view will handle GET and POST HTTP methods in the view(controler)
# @permission_classes([IsAuthenticated]) ## This decorator restricts access to only authenticated users(logged users)
def user_details(request):

    ## Hadle GET request : retreive and return all the users
    if request.method == 'GET':
        ## Query all the users from the db
        users = UserDetails.objects.all()

        ## Serialize the queryset to JSON format
        serializer = UserDetailsSerializer(users,many = True)

        ## Return the serialized data as JSON response
        return Response(serializer.data)

    ## Handle POST request : creaet a new user 
    elif request.method == 'POST':
    
        ## deserialize and validate the input data from the request body
        userSerializer  = UserDetailsSerializer(data=request.data)

        ## Check if the input data is valid
        if userSerializer.is_valid():
            ## Save the user to DB
            userSerializer.save()

            ## Return the saved entry with the succeful statis code
            return Response(userSerializer.data,status=status.HTTP_201_CREATED)

        ## If the data is not valid, return validation erros with a 400 BAD  request
        return Response(userSerializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PUT','DELETE']) ## This decorator specifies  the view will handle GET,PUT AND DELETE Methods
# @permission_classes([IsAuthenticated])## This decorator restricts only authnticated users to access the view
def get_user(request,pk):
    try:
        ## retrieve the user by id
        user  = UserDetails.objects.get(pk=pk)
    except UserDetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND) ## If the user not found 
    
    ## Get a single user by ID
    if request.method == 'GET':
        ## Serialize the query  to json format
        userSerializer = UserDetailsSerializer(user)
        return Response(userSerializer.data)
    ## Update user details
    elif request.method == 'PUT':
        ## Deserialize the Incoming json rwquest input data and validate them
        userUpdateSerializer = UserDetailsSerializer(user,data=request.data,partial=True)
        if userUpdateSerializer.is_valid():
            ## save the updated data 
            userUpdateSerializer.save()
            return Response(userUpdateSerializer.data)

        return Response(userUpdateSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

    ## Delete user
    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
def role_type(request):

    if request.method == 'GET':
        roleTypes = RoleType.objects.all()
        role_serializer = RoleTypeSerializer(roleTypes,many=True)
        return Response(role_serializer.data)
    elif request.method == 'POST':
        roleSerializer = RoleTypeSerializer(data=request.data)

        if roleSerializer.is_valid():
            roleSerializer.save()
            return Response(roleSerializer.data,status=status.HTTP_201_CREATED)
        return Response(roleSerializer.errors,status=status.HTTP_400_BAD_REQUEST)

## view to update and delete a role type
@api_view(['PUT','DELETE'])
# @permission_classes([IsAuthenticated])
def update_or_delete_role(request,pk):

    try:
        ## get the Role type By Id
        role_type = RoleType.objects.get(pk=pk)
    except RoleType.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        roleUpdateSerializer = RoleTypeSerializer(role_type,data=request.data,partial=True)

        if roleUpdateSerializer.is_valid():
            roleUpdateSerializer.save()
            return Response(roleUpdateSerializer.data)
        return Response(roleUpdateSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        role_type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

## View to get and add Status
@api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
def get_or_add_status(request):
    if request.method == 'GET':
        statuses = Status.objects.all()
        staus_serializer = StatusSerializer(statuses,many=True)
        return Response(staus_serializer.data)
    elif request.method == 'POST':
        status_add_serializer = StatusSerializer(data = request.data)

        if status_add_serializer.is_valid():
            status_add_serializer.save()
            return Response(status_add_serializer.data,status=status.HTTP_201_CREATED)
        return Response(status_add_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


## view to update and delete  status
@api_view(['GET','POST'])
# @permission_classes([IsAuthenticated])
def update_or_delete_status(request,pk):
    try:
        ## get the Status By Id
        status = Status.objects.get(pk=pk)
    except Status.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        statusUpdateSerializer = StatusSerializer(status,data=request.data,partial=True)

        if statusUpdateSerializer.is_valid():
            statusUpdateSerializer.save()
            return Response(statusUpdateSerializer.data)
        return Response(statusUpdateSerializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        status.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

## api view to get user by email
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_user_by_email(request):
    ## get the email from request query params
    email = request.query_params.get('email')

    if not email:
        return Response({"error":"Email is required"},status=status.HTTP_400_BAD_REQUEST)

    try:
        user = UserDetails.objects.get(Email = email)
        userByEmailSerializer = UserDetailsSerializer(user)
        return Response(userByEmailSerializer.data)
    except UserDetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    

## api view to login a user
@api_view(['POST'])
def user_login(request):

    login_serializer = LoginSerializer(data=request.data)

    if login_serializer.is_valid():
        email = login_serializer.validated_data['Email']
        password = login_serializer.validated_data['Password']

        ## check credentials
        user = login_user(email,password)

        ## token generation
        if user:
            token = generate_token(user)

            return Response({
            'message':'Login succesfull',
            'token':token,
            
            },status=status.HTTP_200_OK)

        else:
            return Response({
            'Error':'Invalid Credentials',

            },status=status.HTTP_401_UNAUTHORIZED)
    
    return Response(login_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

