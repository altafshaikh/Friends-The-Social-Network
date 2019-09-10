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
from django.views.generic.base import View

class IndexView(View):

    def get(self, request, *args, **kwargs):
        context = {"posts":[]}
        post_list=[]
        post_like_list=[]
        if not self.request.user == None:
            user = self.request.user
            pro_id = self.request.user.profile.id
            usr_pro = Profile.objects.filter(pk=pro_id)[0]
            usr_follow = FollowUser.objects.filter(followed_by=usr_pro)
            usr_post_liked = PostLike.objects.filter(liked_by=usr_pro.user)
            print(usr_post_liked)
            for profile in usr_follow:
                following_usr = profile.profile.user
                post = Post.objects.filter(upload_by=following_usr)[0]
                post_list.append(post)

            for usr_liked in usr_post_liked:
                liked_usr_post = usr_liked.post
                print(liked_usr_post)
                # post = Post.objects.filter(upload_by=liked_usr)[0]
                post_like_list.append(liked_usr_post)
            
            context["posts"]=post_list
            context["post_likes"]=post_like_list
            context["user"] =user
        print(context)
        return render(request, "registration/index.html", context=context)

    

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

def post_create(request):
    print(request.method == 'POST')
    if (request.method == 'POST'):
        form = forms.PostCreateForm(request.POST, request.FILES)

        # print(form.errors)#most helpfull statement help me to slove the error
        if (form.is_valid()):
            
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.upload_by= request.user
            
            user.subject = form.cleaned_data.get('subject')
            user.msg = form.cleaned_data.get('msg')

            user.pic = form.cleaned_data.get('pic')
            user.save()
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
        return Profile.objects.filter(Q(name__icontains = si) | Q(gender__icontains = si) | Q(status__icontains = si) | Q(age__icontains = si)).filter(~Q(id__in=[1,self.request.user.profile.id])).order_by("-id")

    def get_context_data(self, *args, **kwargs):
        context = super(ProfileListView, self).get_context_data(*args, **kwargs)
        context["profile_list"]=Profile.objects.all().filter(~Q(id__in=[1,self.request.user.profile.id])).order_by("-id")
        pro_id = self.request.user.profile.id
        usr_pro = Profile.objects.filter(pk=pro_id)[0]
        usr_follow = FollowUser.objects.filter(followed_by=usr_pro)

        following_list = []
        for profile in usr_follow:
            following_usr = profile.profile.user
            following_list.append(following_usr)

        context['follow_list'] = following_list
        print(context)
        return context

class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'core/profile_detail.html'

def follow(request,pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user,followed_by=request.user.profile)
    return HttpResponseRedirect(redirect_to = "/profile/")
def unfollow(request,pk):
    user = Profile.objects.get(pk=pk)
    criterion1 = Q(profile=user)
    criterion2 = Q(followed_by=request.user.profile)
    obj = FollowUser.objects.filter(criterion1 & criterion2)
    # print(obj[0].profile)
    obj.delete()
    return HttpResponseRedirect(redirect_to = "/profile/")

def like(request,pk):
    usr= request.user
    user_post = Post.objects.get(pk=pk)
    count = user_post.count
    user_post.count = count+1
    user_post.save()
    PostLike.objects.create(post=user_post,liked_by=usr)
    return HttpResponseRedirect(redirect_to = "/")

def dislike(request,pk):
    user_post = Post.objects.get(pk=pk)
    criterion1 = Q(post=user_post)
    criterion2 = Q(liked_by=request.user)
    obj = PostLike.objects.filter(criterion1 & criterion2)
    count = user_post.count
    user_post.count = count-1
    user_post.save()
    obj.delete()
    return HttpResponseRedirect(redirect_to = "/")


def comment(request,pk):
    usr = request.user
    if (request.method == 'POST'):
        
        form = forms.CommentCreateForm(request.POST)
        if (form.is_valid()):

            commented_by= usr
            msg = form.cleaned_data.get('msg')
        
            user_post = Post.objects.get(pk=pk)
            post = user_post

            user_post = Post.objects.get(pk=pk)
            count = user_post.count
            user_post.count = count+1
            user_post.save()

            Comment.objects.create(post=post,commented_by=commented_by,msg=msg)

            return redirect("/")
    else:
       
        form = forms.CommentCreateForm()
    
    return render(request, 'core/comment.html', {'form': form})


# class ProfileDetailView(DetailView):
#     model = Profile
#     template_name = 'core/profile_detail.html'