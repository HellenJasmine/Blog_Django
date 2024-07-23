from django.urls import path
from blog.views import *


app_name = 'blog'

urlpatterns = [
    path("", index, name='index'),
    path("page/<slug:slug>", page, name='page'),
    path("post/<slug:slug>/", post, name='post'),

    path("created_by/<int:author_pk>/", created_by, name='created_by'),
    path("category/<slug:slug>/", category, name='category'),
    
]
