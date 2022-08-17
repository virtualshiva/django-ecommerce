"""ecommerce_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from wsgiref.simple_server import demo_app
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def index(request):
    return HttpResponse('This is a custom page designed')

def result(request):
    a = 10
    b = 20
    c = ('result is :', a+b)
    return HttpResponse(c)

urlpatterns = [
    path('admin/user', admin.site.urls),
    path('test/',index),
    path('hello/',result),
    path('admin/',include('demo_app.urls')),
    path('', include('accounts.urls')),
    path('', include('userspage.urls')),
]
