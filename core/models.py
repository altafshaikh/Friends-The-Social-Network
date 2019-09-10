from django.contrib import auth
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Permission, User
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator, MinValueValidator
# from django.contrib.auth.models import UserManager


class Profile(models.Model):
    name = models.CharField(max_length =100)
    user = models.OneToOneField(to=User,on_delete =CASCADE)
    age = models.IntegerField(default=18, validators=[MinValueValidator(18)])
    phone_no = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")],max_length=15)
    status = models.CharField(max_length =20, default="single", choices=(("single","single"),("married","married"),("commited","commited")))
    gender = models.CharField(max_length =20, default="male", choices=(("male","male"),("female","female")))
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to="images/",null=True)
    
    def __str__(self):
        return "%s" % (self.user)


@receiver(post_save, sender=User)
def save_profie(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance, name = instance.username)
    instance.profile.save()


class Post(models.Model):
    pic = models.ImageField(upload_to="images/",null=True, blank=True)
    subject = models.TextField(max_length=200)
    msg = models.TextField(null=True, blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    upload_by = models.ForeignKey(to=User, on_delete= CASCADE,null=True, blank=True)
    
    def __str__(self):
        return "%s" % (self.subject)

class Comment(models.Model):
    post = models.ForeignKey(to=Post, on_delete= CASCADE)
    msg = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to="images/",null=True)
    subject = models.TextField(max_length=200)
    commented_by = models.ForeignKey(to=User, on_delete= CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    flag = models.CharField(max_length =20, null=True,blank=True, choices=(("racist","racist"),("abusive","abusive")))
    
    def __str__(self):
        return "%s" % (self.msg)

class PostLike(models.Model):
    post = models.ForeignKey(to=Post, on_delete= CASCADE)
    count = models.IntegerField(default=0)
    liked_by = models.ForeignKey(to=User, on_delete= CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s" % (self.liked_by)

class FollowUser(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete= CASCADE,related_name="profiles")
    followed_by = models.ForeignKey(to=Profile, on_delete= CASCADE,related_name="followed_by")

    def __str__(self):
        return "%s" % (self.followed_by)   