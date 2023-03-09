from django import template
from dashboard.models import Profile
# from atexit import register
register=template.Library()
@register.filter(name='get_val')
def get_val(dict,key):
    return dict.get(key)

@register.filter(name='get_prof')
def get_prof(user):
    return Profile.objects.get(user=user)

@register.filter(name='get_like')
def get_like(likedict,key):
    return likedict.get(str(key))

@register.filter(name='get_comment')
def get_comment(commentdict,key):
    return commentdict.get(str(key))

@register.filter(name='get_sport')
def get_sport(sportdict,key):
    return sportdict.get(key)

@register.filter(name='get_hobby')
def get_hobby(hobbydict,key):
    return hobbydict.get(key)

@register.filter(name='get_gender')
def get_gender(genderdict,key):
    return genderdict.get(key)

