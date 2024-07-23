from django.contrib import admin 
from django.urls import path
from blog.views import *


app_name = 'blog'

urlpatterns = [
    path("", index, name='index'),
    path("page/", page, name='page'),
    path("post/<slug:slug>/", post, name='post'),
]
