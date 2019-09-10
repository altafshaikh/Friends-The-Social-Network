from django.urls import reverse,reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView, TemplateView, UpdateView, ListView, DetailView, DeleteView
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

# @method_decorator(login_required, name="dispatch")
# class PostCreateView(CreateView):
#     model = Post
#     template_name = "core/create_post.html"
#     fields = ["subject","msg","pic"]

#     def form_valid(self,form):
#         self.object = form.save()
#         self.object.upload_by = self.request.user.profile
#         self.object.save()
#         return HttpResponseRedirect(reverse_lazy('core:post'))

def post_create(request):
    print(request.method == 'POST')
    if (request.method == 'POST'):
        form = forms.PostCreateForm(request.POST, request.FILES)

        # print(form.errors)#most helpfull statement help me to slove the error
        if (form.is_valid()):
            print("why i am not here")
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.upload_by= request.user
            
            user.subject = form.cleaned_data.get('subject')
            user.msg = form.cleaned_data.get('msg')
            print(form.cleaned_data.get('pic'))
            user.pic = form.cleaned_data.get('pic')
            user.save()
            print("i reached here")
            #post_list = Post.objects.filter(Q(upload_by = self.request.user)).filter(Q(subject__icontains = si) | Q(msg__icontains = si)).order_by("-id")
            return redirect("post")
    else:
        form = forms.PostCreateForm()
        print("i am returning fro here")
    return render(request, 'core/create_post.html', {'form': form})

@method_decorator(login_required, name="dispatch")
class PostListView(ListView):
    model = Post
    template_name = "core/list_post.html"

    def get_queryset(self):
        si = self.request.GET.get("si")
        if si==None:
            si=""
        return Post.objects.filter(Q(upload_by = self.request.user)).filter(Q(subject__icontains = si) | Q(msg__icontains = si)).order_by("-id")
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'core/post_detail.html'

class PostDeleteView(DeleteView):
    model = Post

@method_decorator(login_required, name="dispatch")
class ProfileListView(ListView):
    model = Profile
    template_name = "core/profile_list.html"

    def get_queryset(self):
        si = self.request.GET.get("si")
        if si==None:
            si=""
        return Profile.objects.filter(Q(name__icontains = si) | Q(gender__icontains = si) | Q(status__icontains = si) | Q(age__icontains = si)).order_by("-id")


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'core/profile_detail.html'

def follow(request,pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user,followed_by=request.user.profile)
    return HttpResponseRedirect(redirect_to = "/profile/")