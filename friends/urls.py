from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from core import views as core_views
from friends import settings

urlpatterns = [
    url(r"^$", core_views.IndexView.as_view(), name="index"),
    path("profile/edit/<int:pk>", core_views.ProfileUpdateView.as_view(success_url="/"), name='editprofile'),
    path("user/post/", include('core.urls')),
    # path("user/post/done",core_views.PostDoneView.as_view(),name="done"),
    # path("post/create/", core_views.PostCreateView.as_view(success_url="/post/"), {'template_name': 'core/create_post.html'}, name='createpost'),
    path("post/", core_views.PostListView.as_view(), name='post'),
    url(r'^login/$', auth_views.LoginView.as_view(),{'template_name': 'core/login.html'}, name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(),{'template_name': 'core/logout.html'}, name='logout'),
    url(r"^signup/$", core_views.signup, name="signup"),
    url(r'^admin/', admin.site.urls),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
