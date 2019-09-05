from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from django.views.generic import CreateView, TemplateView
from . import forms

class IndexView(TemplateView):
    template_name = 'registration/index.html'


class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"