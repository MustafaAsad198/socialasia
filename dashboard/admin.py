from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import Profile ,Post,Like,Follow,Dm,Postcomment,Predictmatch,Piro,Notification,Networkgraph,Caption,Examplecaption,Hub,HubDm,Meeting
class PostAdmin(admin.ModelAdmin):
    list_display=('id','user','image_tag','caption','time','likes')

class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','userid','bio','location','pfp_tag','sport','hobbies','age','gender','in_meeting')

class PiroAdmin(admin.ModelAdmin):
    list_display=('user','since','type')

class NotificationAdmin(admin.ModelAdmin):
    list_display=('ntype','timestamp','nfromuser','ntouser','tohub','meeting')

class CaptionAdmin(admin.ModelAdmin):
    list_display=('sno','inpimage')

class ExamplecaptionAdmin(admin.ModelAdmin):
    list_display=('sno','user','text','contentlength','obj')

class HubAdmin(admin.ModelAdmin):
    list_display=('sno','name','head','get_members')
    def get_queryset(self, request):
        qs= super().get_queryset(request)
        return qs.prefetch_related('members')
    def get_members(self, obj):
        return ','.join([m.username for m in obj.members.all()])

class HubDmAdmin(admin.ModelAdmin):
    list_display=('sno','dm_text','from_user','hub','parent','timestamp')

class MeetingAdmin(admin.ModelAdmin):
    list_display=('id','title','host','created_time','scheduled_date','scheduled_time','get_participants','is_recurring','recurring_type','last_active_date')
    def get_queryset(self, request):
        qs= super().get_queryset(request)
        return qs.prefetch_related('participants')
    def get_participants(self, obj):
        return ','.join([p.username for p in obj.participants.all()])

# Register your models here.
admin.site.register(Profile,ProfileAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Dm)
admin.site.register(Postcomment)
admin.site.register(Predictmatch)
admin.site.register(Piro)
admin.site.register(Notification,NotificationAdmin)
admin.site.register(Networkgraph)
admin.site.register(Caption,CaptionAdmin)
admin.site.register(Examplecaption,ExamplecaptionAdmin)
admin.site.register(Hub,HubAdmin)
admin.site.register(HubDm,HubDmAdmin)
admin.site.register(Meeting,MeetingAdmin)