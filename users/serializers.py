from rest_framework import serializers ## Module which can be used to convert python data objets into json type and json type into python objects
from .models import UserDetails,RoleType,Status

## Serializer for RoleType model

class RoleTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleType
        fields = ['RoleID','RoleName','Status','CreatedAt','UpdatedAt']

## Serializer for Status model
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['StatusID','StatusName','CreatedAt','UpdatedAt']

## Serializer for UserDetails model
class UserDetailsSerializer(serializers.ModelSerializer):
    ## Nested serializers for read - only representation
    role_type = RoleTypeSerializer(read_only = True) ## display RoleType object
    status = StatusSerializer(read_only = True) ## display Status Object

    ## allow POST/PUT by referencing related models via their primary keys
    roleType_id = serializers.PrimaryKeyRelatedField(
        queryset = RoleType.objects.all(), ## accepts RoleType ID as input
        source = "RoleType" ## maps the actual model class
    )

    status_id = serializers.PrimaryKeyRelatedField(
        queryset  = Status.objects.all(), ## accepts status ID as input
        source = "Status" ## map the actual model class
    )


    class Meta:
        model = UserDetails
        fields = ['UserID', 'FirstName', 'LastName', 'Email', 'Password', 'DateofBirth',
            'role_type', 'roleType_id',  # both readable and writable role info
            'status', 'status_id',      # both readable and writable status info
            'CreatedAt', 'UpdatedAt'
        ]

## Serializer used during login
class LoginSerializer(serializers.Serializer):
    Email = serializers.EmailField() ## accepts only email format
    Password = serializers.CharField(write_only=True) ## paswords will not return in response