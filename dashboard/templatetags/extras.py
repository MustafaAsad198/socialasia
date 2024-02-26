from django import template
from dashboard.models import Profile
from datetime import datetime
# from atexit import register
register=template.Library()
@register.filter(name='get_val')
def get_val(val_dict,key):
    return val_dict.get(key)

@register.filter(name='get_prof')
def get_prof(user):
    return Profile.objects.get(user=user)

@register.filter(name='get_like')
def get_like(like_dict,key):
    return like_dict.get(str(key))

@register.filter(name='get_comment')
def get_comment(comment_dict,key):
    return comment_dict.get(str(key))

@register.filter(name='get_sport')
def get_sport(sport_dict,key):
    return sport_dict.get(key)

@register.filter(name='get_hobby')
def get_hobby(hobby_dict,key):
    return hobby_dict.get(key)

@register.filter(name='get_gender')
def get_gender(gender_dict,key):
    return gender_dict.get(key)

@register.filter(name='get_24_hours_time')
def get_24_hours_time(time):
    time=time.strftime("%H:%M %p")
    t=datetime.strptime(time,"%H:%M %p")
    return t.strftime("%H:%M")

@register.filter(name='get_date')
def get_date(date):
    return date.strftime("%Y-%m-%d")

@register.filter(name='get_authorised_user')
def get_authorised_user(auth_users,user):
    return
