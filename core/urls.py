from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from . import views


app_name="core"

urlpatterns = [

  path("", views.IndexView.as_view(), name="index"),
  path("create/", views.post_create, name='createpost'),
  # path("post/", views.PostListView.as_view(), name='post'),

  
]