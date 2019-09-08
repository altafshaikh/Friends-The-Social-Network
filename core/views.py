from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from . import forms
from core.models import Post, PostLike, Profile, Comment, FollowUser
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

class IndexView(TemplateView):
    template_name = 'registration/index.html'

@method_decorator(login_required, name="dispatch")
class ProfileUpdateView(UpdateView):
    model = Profile
    template_name = "core/profile_form.html"
    fields = ["name","user","age","phone_no","status","gender","address","description","pic"]

def signup(request):
    if request.method == 'POST':
        form = forms.UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.name = form.cleaned_data.get('name')
            # user.profile.user = form.cleaned_data.get('username')
            user.profile.phone_no = form.cleaned_data.get('phone_no')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = forms.UserCreateForm()
    return render(request, 'registration/signup.html', {'form': form})



# class SignUp(CreateView):
#     form_class = forms.UserCreateForm
#     success_url = reverse_lazy("login")
#     template_name = "registration/signup.html"