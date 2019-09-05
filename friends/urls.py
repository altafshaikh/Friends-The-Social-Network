from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from core import views as core_views
urlpatterns = [
    url(r"^$", core_views.IndexView.as_view(), name="index"),
    url(r'^login/$', auth_views.LoginView.as_view(),{'template_name': 'core/login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(),{'template_name': 'core/logout.html'}, name='logout'),
    url(r"^signup/$", core_views.SignUp.as_view(), name="signup"),
    url(r'^admin/', admin.site.urls),
]
