"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from users.views import (
    user_details,
    get_user,
    role_type,
    update_or_delete_role,
    get_or_add_status,
    update_or_delete_status,
    get_user_by_email,
    user_login


)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users',user_details,name='users-details'),
    path('api/users/<int:pk>',get_user,name='get-user-by-id'),
    path('api/roles',role_type,name='role-types'),
    path('api/roles/<int:pk>',update_or_delete_role,name='role-update-delete'),
    path('api/statuses',get_or_add_status,name='status-details'),
    path('api/statuses/<int:pk>',update_or_delete_status,name='status-delete-or-update'),
    path('api/users/email',get_user_by_email,name='get-user-by-email'),

    path('api/login',user_login,name='login')
]
