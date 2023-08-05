from django.contrib import admin
from django.urls import path,include
from . import views
urlpatterns = [
    path('',views.index,name='dashboard-index'),
    path('register/',views.register,name='register'),
    path('login/',views.customlogin,name='login'),
    path('logout/',views.customlogout,name='logout'),
    path('settings/',views.settings,name='settings'),
    path('accountsettings/',views.accountsettings,name='accountsettings'),
    path('upload/',views.upload,name='upload'),
    path('like/',views.like,name='like'),
    path('postcomment/',views.postcomment,name='postcomment'),
    path('profile/<str:pk>',views.profile,name='profile'),
    path('follow/',views.follow,name='follow'),
    path('search/',views.search,name='search'),
    path('dms/',views.dms,name='dms'),
    path('dms/<str:slug>',views.dm,name='dm'),
    path('dms/postdm/',views.postdm,name='postdm'),
    path('dms/dmsearch/',views.dmusersearch,name='dmusersearch'),
    path('predict/<str:slug>',views.predict,name='predict'),
    path('postdelete',views.postdelete,name='postdelete'),
    path('dmdelete',views.dmdelete,name='dmdelete'),
    path('piro',views.piro,name='piro'),
    path('pirocreate',views.pirocreate,name='pirocreate'),
    path('notifdeletefollow',views.notifdeletefollow,name='notifdeletefollow'),
    path('notifdeletedm',views.notifdeletedm,name='notifdeletedm'),
    path('notifaccept',views.notifaccept,name='notifaccept'),
    path('networkgraphcreate/<int:sno>',views.networkgraphcreate,name='networkgraphcreate'),
    path('caption',views.caption,name='caption'),
    

]