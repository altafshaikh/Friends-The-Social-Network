from django.contrib import admin
from core.models import FollowUser, Post, PostLike, Profile, Comment
from django.contrib.admin.options import ModelAdmin

class FollowUserAdmin(ModelAdmin):
    list_display = ["profile","followed_by"]
    search_fields = ["profile","followed_by"]
    list_filter = ["profile","followed_by"]
admin.site.register(FollowUser, FollowUserAdmin)


class PostAdmin(ModelAdmin):
    list_display = ["subject","upload_by","cr_date"]
    search_fields = ["subject","upload_by"]
    list_filter = ["cr_date","upload_by"]
admin.site.register(Post, PostAdmin)

class PostLikeAdmin(ModelAdmin):
    list_display = ["liked_by","post"]
    search_fields = ["liked_by","post"]
    list_filter = ["cr_date"]
admin.site.register(PostLike, PostLikeAdmin)

class ProfileAdmin(ModelAdmin):
    list_display = ["name"]
    search_fields = ["name","status","phone_no"]
    list_filter = ["status","gender"]
admin.site.register(Profile, ProfileAdmin)

class CommentAdmin(ModelAdmin):
    list_display = ["post","msg"]
    search_fields = ["msg","post","commented_by"]
    list_filter = ["cr_date"]
admin.site.register(Comment, CommentAdmin)
