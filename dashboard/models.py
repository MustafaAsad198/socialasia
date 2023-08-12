from operator import mod
from re import T
from statistics import mode
from tabnanny import check
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
import uuid
from django.db.models import CheckConstraint,Q,F
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator,MinValueValidator
from django import forms
# Create your models here.
SPORT=(
    (50,'None'),
    (51,'Football'),
    (52,'Hockey'),
    (53,'Cricket'),
    (54,'Basketball'),
    (55,'Rugby'),
    (56,'Volleyball'),
    (57,'Prefer Video Games'),
    (58,'Badminton'),
    (59,'Tennis'),
    (599,'Table Tennis'),
)
HOBBY=(
    (80,'None'),
    (81,'Dancing'),
    (82,'Singing'),
    (83,'Acting'),
    (84,'Reading'),
    (85,'Drawing'),
    (86,'Writing'),
    (87,'Swimming'),
)
GENDER=(
    (-1,'Prefer not to disclose'),
    (0,'Female'),
    (1,'Male'),
)
PTYPE=(
    (71,'Classic'),
    (72,'Booster'),
    (73,'Premium'),
)
NTYPE=(
    (90,'None'),
    (91,'Follow'),
    (92,'Message'),
)
LTYPE=(
    (11,'Long'),
    (12,'Medium'),
    (13,'Short'),
)
OTYPE=(
    (61,'Mountain'),
    (62,'Street'),
    (63,'Glacier'),
    (64,'Building'),
    (65,'Sea'),
    (66,'Forest'),
)
class Profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    userid=models.IntegerField()
    bio=models.TextField(blank=True)
    location=models.CharField(max_length=50,blank=True)
    pfp=models.ImageField(default='avatar.jpg',upload_to='profile_images')
    sport=models.PositiveIntegerField(default=50,choices=SPORT)
    hobbies=models.PositiveIntegerField(default=80,choices=HOBBY)
    age=models.PositiveIntegerField()
    gender=models.IntegerField(default=-1,choices=GENDER)
    private=models.BooleanField(default=False)

    class Meta:
        constraints=[CheckConstraint(check=Q(age__gte=18),name='age_gte_18')]

    def __str__(self):
        return self.user.username
    
    def pfp_tag(self):
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.pfp))
    

class Post(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='post_images')
    caption=models.TextField(blank=True)
    time=models.DateTimeField(auto_now_add=True)
    likes=models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user} posted image {self.image}, saying {self.caption} at {self.time}'
    
    def image_tag(self):
        return mark_safe('<img src="/../../media/%s" width="150" height="150" />' % (self.image))


class Like(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    postid=models.ForeignKey(Post,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} liked {self.postid}'

class Follow(models.Model):
    follower=models.ForeignKey(User,on_delete=models.CASCADE,related_name='follower')
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    requested=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.follower} follows {self.user}- request is {self.requested}'
    
class Dm(models.Model):
    sno=models.AutoField(primary_key=True)
    dmtext=models.TextField(blank=False)
    fromuser=models.ForeignKey(User,on_delete=models.CASCADE,related_name='fromuser')
    touser=models.ForeignKey(User,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    fpfp=models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self) -> str:
        return f'{self.fromuser} texted {self.touser} - {self.dmtext[:30]} on {self.timestamp}'
    
    class Meta:
        ordering=['-timestamp']

class Postcomment(models.Model):
    postid=models.ForeignKey(Post,on_delete=models.CASCADE)
    comment=models.TextField(blank=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)    

    def __str__(self) -> str:
        return f'{self.user} commented on {self.postid} saying - {self.comment}'


class Predictmatch(models.Model):
    user1=models.ForeignKey(User,on_delete=models.CASCADE,related_name='currentuser')
    user2=models.ForeignKey(User,on_delete=models.CASCADE)
    sport1=models.PositiveIntegerField(null=True)
    sport2=models.PositiveIntegerField(null=True)
    hobbies1=models.PositiveIntegerField(null=True)
    hobbies2=models.PositiveIntegerField(null=True)
    age1=models.PositiveIntegerField(null=True)
    age2=models.PositiveIntegerField(null=True)
    gender1=models.IntegerField(null=True)
    gender2=models.IntegerField(null=True)
    result=models.CharField(blank=True,max_length=50)

    def __str__(self) -> str:
        return f'{self.user1} matched with {self.user2}'

class Piro(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    since=models.DateField(auto_now_add=True)
    type=models.PositiveIntegerField(blank=True,choices=PTYPE)

    def __str__(self):
        return f'{self.user} is a {self.type} user since {self.since}'

class Notification(models.Model):
    sno=models.AutoField(primary_key=True)
    ntype=models.PositiveIntegerField(choices=NTYPE,default=90)
    timestamp=models.DateTimeField(auto_now_add=True)
    nfromuser=models.ForeignKey(User,on_delete=models.CASCADE,related_name='nfromuser')
    ntouser=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.ntouser} has notification from {self.nfromuser} for {self.ntype}'

    class Meta:
        ordering=['-timestamp']

class Networkgraph(models.Model):
    sno=models.AutoField(primary_key=True)
    src=models.ForeignKey(User,on_delete=models.CASCADE)
    level=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(4)])

    def __str__(self) -> str:
        return f'graph {self.sno} for {self.src}'

class Caption(models.Model):
    sno=models.AutoField(primary_key=True)
    inpimage=models.ImageField(upload_to='caption_images')

    def __str__(self) -> str:
        return f'{self.sno} - {self.inpimage}'

class Examplecaption(models.Model):
    sno=models.AutoField(primary_key=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    text=models.TextField(blank=False)
    contentlength=models.PositiveIntegerField(choices=LTYPE)
    obj=models.PositiveIntegerField(choices=OTYPE)

    def __str__(self) -> str:
        return f'{self.obj} - {self.text} has length {self.contentlength} by {self.user}'