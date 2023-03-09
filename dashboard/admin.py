from django.contrib import admin
from .models import Profile ,Post,Like,Follow,Dm,Postcomment,Predictmatch,Piro,Notification,Networkgraph
class PostAdmin(admin.ModelAdmin):
    list_display=('id','user','image_tag','caption','time','likes')

class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','userid','bio','location','pfp_tag','sport','hobbies','age','gender')

class PiroAdmin(admin.ModelAdmin):
    list_display=('user','since','type')

class NotificationAdmin(admin.ModelAdmin):
    list_display=('ntype','timestamp','nfromuser','ntouser')
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
