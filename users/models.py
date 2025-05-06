from django.db import models
from django.core.validators import EmailValidator # built in django module for email validation
from django.contrib.auth.hashers import make_password #built in django module for hash passwords
# Create your models here.

class RoleType(models.Model):
    RoleID = models.AutoField(primary_key=True) #primary key and auto increment
    RoleName  = models.CharField(max_length=100)
    Status = models.IntegerField(default=1)
    CreatedAt = models.DateTimeField(auto_now_add=True) ## recorded when the object was created
    UpdatedAt = models.DateTimeField(auto_now=True) ## record automaticaly on every update

    ## explicitly set the table name 
    class Meta:
        db_table = 'RoleType'
    
    def __str__(self):
        return f"{self.RoleName}" ## Human readable representation when object call
    

class Status(models.Model):
    StatusID = models.AutoField(primary_key=True)
    StatusName = models.CharField(max_length=255)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Status'

    def __str__(self):
        return f"{self.StatusName}"

class UserDetails(models.Model):
    UserID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=255)
    LastName = models.CharField(max_length=255)
    Email = models.CharField(
        unique=True,## ensure no duplicate emails
        max_length=100,
        validators=[EmailValidator()]## validates proper email formats when save to the database
    )
    Password = models.CharField(max_length=255)
    DateofBirth = models.CharField(max_length=20)
    RoleType = models.ForeignKey(RoleType, on_delete=models.CASCADE) ## foreign key linking to the RoleType model
    Status = models.ForeignKey(Status,on_delete=models.CASCADE)
    CreatedAt = models.DateTimeField(auto_now_add=True)
    UpdatedAt = models.DateTimeField(auto_now=True)

    ## explicitly set the table name
    class Meta:
        db_table = 'UserDetails'

    ## override the save function to hash password only when a new user is created
    def save(self,*args,**kwargs):
        if not self.pk or self._state.adding:
            self.Password = make_password(self.Password) ## Hash the password
        super().save(*args,**kwargs) ## call the base class save method


    
    
    ## human readable representation for the object
    def __str__(self):
        return f"{self.FirstName} {self.LastName}"
