from asyncore import read
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile ,Post,Like,Follow,Dm,Postcomment,Predictmatch,Piro,Notification,Networkgraph
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from collections import deque,defaultdict
from itertools import chain
import random
from .forms import ProfileUpdateForm,PredictDataFrom,NetworkGraphPremiumForm,NetworkGraphBoosterForm
from sklearn.tree import DecisionTreeClassifier
import joblib
from dashboard.templatetags import extras
import matplotlib.pyplot as plt
import networkx as nx
from django.db.models import Q
import os
from django.core.mail import send_mail
from django.conf import settings as conf_settings
# Create your views here.
@login_required
def index(request):
    # return HttpResponse('index')
    user=User.objects.get(username=request.user.username)
    userprofile=Profile.objects.get(user=user)
    # print(userprofile)
    allprofiles=Profile.objects.all()
    posts=deque([])
    users=User.objects.all()
    userfollowing=list(Follow.objects.filter(follower=request.user,requested=False).values_list('user',flat=True))
    # print(userfollowing)
    for u in userfollowing:
        uposts=Post.objects.filter(user=u)
        posts.append(uposts)
    random.shuffle(posts)
    posts=list(chain(*posts))
    # print(posts)
    currentfollowingusers=deque([])
    for u in userfollowing:
        currentfollowingusers.append(u)
    # print(currentfollowingusers)
    usersuggestion=[i for i in users if (i.id not in currentfollowingusers and i!=user)]
    random.shuffle(usersuggestion)
    # print(usersuggestion)
    profilesuggestion=deque([])
    for us in usersuggestion:
        profilesuggestion.append(Profile.objects.filter(userid=us.id))
    profilesuggestion=list(chain(*profilesuggestion))
    # print(profilesuggestion)
    likes=Like.objects.all()
    # print(likes)
    likedict={}
    for l in likes:
        if str(l.postid.id) not in likedict:
            likedict[str(l.postid.id)]=[l.user]
        else:
            likedict[str(l.postid.id)].append(l.user)
    # print(likedict)
    comments=Postcomment.objects.all()
    commentdict={}
    for c in comments:
        if str(c.postid.id) not in commentdict:
            commentdict[str(c.postid.id)]=[c]
        else:
            commentdict[str(c.postid.id)].append(c)
    # print(commentdict)
    try:
        pirouser=Piro.objects.get(user=request.user)
    except:
        pirouser=None
    notifics=notifications(request.user)
    notidict={'notifics':notifics}

    if request.method=='POST':
        form=PredictDataFrom(request.POST)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user1=request.user
            instance.sport1=userprofile.sport
            instance.hobbies1=userprofile.hobbies
            instance.age1=userprofile.age
            instance.gender1=userprofile.gender
            user2=form.cleaned_data.get('user2')
            user2profile=Profile.objects.get(user=user2)
            # print(user2profile)
            instance.sport2=user2profile.sport
            instance.hobbies2=user2profile.hobbies
            instance.age2=user2profile.age
            instance.gender2=user2profile.gender
            # print(instance.user1,instance.sport1,instance.hobbies1,instance.age1,instance.gender1,user2,instance.sport2,instance.hobbies2,instance.age2,instance.gender2)
            predicted=Predictmatch.objects.filter(user1=request.user,user2=user2).first()
            if predicted is not None:
                predicted.delete()
            mlmodel=joblib.load('mlmodel/ml_social_model.joblib')
            instance.result= mlmodel.predict([[instance.sport1,instance.sport2,instance.hobbies1,instance.hobbies2,instance.age1,instance.age2,instance.gender1,instance.gender2]])[0].upper()
            # print(instance.result)
            instance.save()
            return redirect(f'/predict/{user2.username}')
    else:
        form=PredictDataFrom()
    formd={}
    if Piro.objects.filter(user=user,type=73).exists():
        src=None
        if request.method=='POST':
            form1=NetworkGraphPremiumForm(request.POST)
            if form1.is_valid():
                level=int(form1.data.get('level'))
                src=form1.data.get('src')
                form1.save()
                recentgraph=Networkgraph.objects.all().last()
                # print(src,form)
                sno=recentgraph.sno
                networkgraph=defaultdict(set)
                q=deque([User.objects.get(id=src)])
                visited=set()
                while q and level>0:
                    for i in range(len(q)):
                        node=q.popleft()
                        if node in visited: continue
                        visited.add(node)
                        for adj in Follow.objects.filter(follower=node):
                            q.append(adj.user)
                            networkgraph[node].add(adj.user)
                    level-=1
                # print(networkgraph)
                # print(os.path.exists(f'media/graph_images/graph{sno}.png'))
                if os.path.exists(f'media/graph_images/graph{sno-1}.png'):
                    os.remove(f'media/graph_images/graph{sno-1}.png')
                    ngdel=Networkgraph.objects.get(sno=sno-1)
                    ngdel.delete()
                G=nx.DiGraph()
                for usernode in networkgraph:
                    for adj in networkgraph[usernode]:
                        G.add_edges_from([(usernode.username,adj.username)])
                for i in list(G.nodes()):
                    G.nodes[i]['length']=len(i)
                node_color = [G.degree(v) for v in G]
                node_size = [500 * nx.get_node_attributes(G, 'length')[v] for v in G]
                nx.draw_networkx(G,node_size=node_size,node_color=node_color, with_labels = True,cmap = plt.cm.Blues,alpha=.8)
                plt.axis('off')
                plt.tight_layout()
                try:
                    plt.savefig(f'media/graph_images/graph{sno}.png', bbox_inches='tight')  
                except:
                    ngdel=Networkgraph.objects.filter(sno=sno).first()
                    ngdel.delete()
                    messages.warning(request,'Unable to create network graph now. Try again later.')
                    return redirect('dashboard-index')
                # plt.show()
                plt.clf()
                return redirect(f'networkgraphcreate/{sno}')
        else:
            form1=NetworkGraphPremiumForm()
        formd['form1']=form1
    elif Piro.objects.filter(user=user,type=72).exists():
        src=None
        if request.method=='POST':
            form2=NetworkGraphBoosterForm(request.POST)
            if form2.is_valid():
                level=int(form2.data.get('level'))
                instance=form2.save(commit=False)
                instance.src=request.user
                instance.save()
                src=request.user
                recentgraph=Networkgraph.objects.all().last()
                # print(src,form)
                sno=recentgraph.sno
                networkgraph=defaultdict(set)
                q=deque([User.objects.get(id=src.id)])
                visited=set()
                while q and level>0:
                    for i in range(len(q)):
                        node=q.popleft()
                        if node in visited: continue
                        visited.add(node)
                        for adj in Follow.objects.filter(follower=node):
                            q.append(adj.user)
                            networkgraph[node].add(adj.user)
                    level-=1
                # print(networkgraph)
                # print(os.path.exists(f'media/graph_images/graph{sno}.png'))
                if os.path.exists(f'media/graph_images/graph{sno-1}.png'):
                    os.remove(f'media/graph_images/graph{sno-1}.png')
                    ngdel=Networkgraph.objects.get(sno=sno-1)
                    ngdel.delete()
                G=nx.DiGraph()
                for usernode in networkgraph:
                    for adj in networkgraph[usernode]:
                        G.add_edges_from([(usernode.username,adj.username)])
                for i in list(G.nodes()):
                    G.nodes[i]['length']=len(i)
                node_color = [G.degree(v) for v in G]
                node_size = [500 * nx.get_node_attributes(G, 'length')[v] for v in G]
                nx.draw_networkx(G,node_size=node_size,node_color=node_color, with_labels = True,cmap = plt.cm.Blues,alpha=.8)
                plt.axis('off')
                plt.tight_layout()
                try:
                    plt.savefig(f'media/graph_images/graph{sno}.png', bbox_inches='tight')  
                except:
                    ngdel=Networkgraph.objects.filter(sno=sno).first()
                    ngdel.delete()
                    messages.warning(request,'Unable to create network graph now. Try again later.')
                    return redirect('dashboard-index')
                # plt.show()
                plt.clf()
                
                return redirect(f'networkgraphcreate/{sno}')
        else:
            form2=NetworkGraphBoosterForm()
        formd['form2']=form2
    context={'userprofile':userprofile,'posts':posts,'allprofiles':allprofiles,'profilesuggestion':profilesuggestion,'likedict':likedict,'commentdict':commentdict,'form':form,'pirouser':pirouser}|notidict|formd
    # print(context)
    return render(request,'index.html',context)

def register(request):
    # return HttpResponse('register')
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        check18=request.POST.getlist('above18check')
        # print('debug')
        # print(check18)
        # print(username)
        # print(email)
        # print(password)

        # return redirect('register')
        if username!='' and password!='' and check18 and password==password2 and email!='':
            
            if User.objects.filter(email=email).exists():
                messages.warning(request,'Email already in use')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.warning(request,'Username already in use')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                userlogin=authenticate(username=username,password=password)
                login(request,userlogin)
                usermodel=User.objects.get(username=username)
                age=18
                profile=Profile.objects.create(user=usermodel,userid=usermodel.id,age=age)
                profile.save()
                messages.info(request,'Please check your age and change if needed. 18 is entered as default age')
                return redirect('settings')
        elif username=='':
            messages.warning(request,'Enter the username')
            return redirect('register')
        elif email=='':
            messages.warning(request,'Enter the email ID')
            return redirect('register')
        
        elif not check18:
            messages.warning(request,'Claim that you are an adult to gain access to this social website')
            return redirect('register')
        elif password =='' or password!=password2:
            messages.warning(request,'Confirmation password did not match with the given password')
            return redirect('register')
    else:
        return render(request,'register.html')


def customlogin(request):
    # return HttpResponse('login')
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            subject='Recent Login Activity has been witnessed with this account'
            message=f'Hello {username}, Thank you for logging in to Socialasia!'
            email_from=conf_settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            # print(recipient_list)
            send_mail( subject, message, email_from, recipient_list )
            return redirect('dashboard-index')
        else:
            messages.warning(request,'Invalid Credentials. Please put down correct username and password')
            return redirect('login')
    return render(request,'login.html')

@login_required
def customlogout(request):
    # return HttpResponse('logout')
    logout(request)
    return redirect('login')

@login_required
def settings(request):
    # return HttpResponse('profile settings')
    userprofile=Profile.objects.get(user=request.user)
    notifics=notifications(request.user)
    notidict={'notifics':notifics}
    if request.method=='POST':
        form = ProfileUpdateForm(request.POST, request.FILES,instance=userprofile)
        if form.is_valid():
            # print(form.data.get('bio'))
            form.save()
            return redirect('dashboard-index')
    else:
            form = ProfileUpdateForm(instance=userprofile)
    # return redirect('settings')
    context={'userprofile':userprofile,'form':form}|notidict
    return render(request,'settings.html',context)

@login_required
def accountsettings(request):
    # return HttpResponse('account settings')
    userprofile=Profile.objects.get(user=request.user)
    if request.method=="POST":
        deluser=request.POST.get('deluser')
        # print(deluser)
        
        User.objects.get(id=deluser).delete()
        return redirect('login')
    context={'userprofile':userprofile}
    return render(request,'accountsettings.html',context)

@login_required
def upload(request):
    # return HttpResponse('upload')
    if request.method=='POST':
        user=request.user
        image=request.FILES.get('imageupload')
        caption=request.POST.get('caption')
        post=Post.objects.create(user=user,image=image,caption=caption)
        post.save()
        return redirect('dashboard-index')
    else:
        return redirect('dashboard-index')

@login_required
def like(request):
    # return HttpResponse('like')
    user=request.user
    postid=request.GET.get('post_id')
    # print(user,postid)
    post=Post.objects.get(id=postid)
    # print(post)
    liked=Like.objects.filter(user=user,postid=post).first()
    # print(liked)
    if liked is None:
        newlike=Like.objects.create(user=user,postid=post)
        newlike.save()
        post.likes=post.likes+1
        post.save()
        return redirect(f'/#post{postid}') #this is also a way of giving url instead of name.
    else:
        liked.delete()
        post.likes=post.likes-1
        post.save()
        return redirect(f'/#post{postid}')

@login_required
def profile(request,pk):
    # return HttpResponse('profile')
    user=User.objects.get(username=pk)
    vieweduserprofile=Profile.objects.get(user=user)
    userposts=Post.objects.filter(user=user)
    viewer=request.user
    userprofile=Profile.objects.get(user=User.objects.get(username=request.user.username))
    if Follow.objects.filter(follower=viewer,user=user,requested=False).first():
        followbutton='Unfollow'
    else:
        followbutton='Follow'
    followers=Follow.objects.filter(user=user,requested=False)
    following=Follow.objects.filter(follower=user,requested=False)
    # print(followers,following)
    followersprofile=deque([])
    for f in followers:
        followersprofile.append(Profile.objects.get(user=f.follower))
    followersprofile=list(followersprofile)
    # print(followersprofile)
    followingprofile=deque([])
    for f in following:
        followingprofile.append(Profile.objects.get(user=f.user))
    followingprofile=list(followingprofile)
    # print(followingprofile)
    pirouser=None
    pirouser=Piro.objects.filter(user=user).first()
    notifics=notifications(request.user)
    notidict={'notifics':notifics}
    # print(notifics)
    if request.method=='POST':
        postids=request.POST.getlist('delcheck')
        # print(postids)
        for postid in postids:
            post=Post.objects.get(id=postid)
            post.delete()
            messages.success(request,'Posts Deleted.')
        return redirect(f'/profile/{request.user.username}')
    context={'vieweduserprofile':vieweduserprofile,'userposts':userposts,'followbutton':followbutton,'followersprofile':followersprofile,'followingprofile':followingprofile,'userprofile':userprofile,'pirouser':pirouser}|notidict
    # print(context)
    return render(request,'profile.html',context)

@login_required
def follow(request):
    # return HttpResponse('follow')
    if request.method=='POST':
        follower=request.POST.get('follower')
        user=request.POST.get('user')
        # print(follower,user)
        if follower==user:
            messages.warning(request,'You cannot follow yourself.')
            return redirect('/profile/'+user)
        else:
            if Follow.objects.filter(follower=User.objects.get(username=follower),user=User.objects.get(username=user),requested=False).first():
                deletefollower=Follow.objects.get(follower=User.objects.get(username=follower),user=User.objects.get(username=user),requested=False)
                deletefollower.delete()
                
                messages.warning(request,f'You have stopped following {user}.')
                return redirect('/profile/'+user)
            else:
                if Profile.objects.get(user=User.objects.get(username=user)).private:
                    newfollower,created= Follow.objects.get_or_create(follower=User.objects.get(username=follower),user=User.objects.get(username=user),requested=True)
                    # print(newfollower)
                    if created:
                        newnotif=Notification.objects.create(ntype=91,nfromuser=newfollower.follower,ntouser=newfollower.user)
                        newfollower.save()
                        newnotif.save()
                        messages.warning(request,f'Follow request has been sent to {user}.')
                    else:
                        messages.warning(request,f'Your follow request is already existing with {user}, wait for their response.')
                else:
                    newfollower=Follow.objects.create(follower=User.objects.get(username=follower),user=User.objects.get(username=user),requested=False)
                    newfollower.save()
                    messages.warning(request,f'You are following {user} now!')

                return redirect('/profile/'+user)
        
    return redirect('/')

@login_required
def search(request):
    # return HttpResponse('search')
    userprofile=Profile.objects.get(user=User.objects.get(username=request.user.username))
    notifics=notifications(request.user)
    notidict={'notifics':notifics}
    if request.method=='POST':
        username=request.POST.get('username')
        searcheduser=User.objects.filter(username__icontains=username)
        # print(searcheduser)
        searcheduserprofiles=deque([])
        for su in searcheduser:
            searcheduserprofiles.append(Profile.objects.filter(userid=su.id))
        searcheduserprofiles=list(chain(*searcheduserprofiles))
        # print(searcheduserprofiles)
        context={'userprofile':userprofile,'searcheduserprofiles':searcheduserprofiles,'username':username}|notidict
        return render(request,'search.html',context)
    else:
        return redirect('/')

@login_required
def dms(request):
    # return HttpResponse('dms')
    userprofile=Profile.objects.get(user=request.user)
    notifics=notifications(request.user)
    # print(notifics)
    notidict={'notifics':notifics}
    allotherprofiles=Profile.objects.all().exclude(user=userprofile.user)
    # print(allotherprofiles)
    alldms=Dm.objects.all()
    # print(alldms,len(alldms))
    recentusers=set()
    fromusers=deque([])
    for dm in alldms:
        if dm.touser==request.user or dm.fromuser==request.user:
            if dm.touser==request.user:
                fromuser=dm.fromuser
                touser=request.user
                if fromuser in recentusers: continue
                fromusers.append(dm)
                recentusers.add(fromuser)
            else:
                fromuser=request.user
                touser=dm.touser
                if touser in recentusers: continue
                fromusers.append(dm)
                recentusers.add(touser)
    # print(fromusers,recentusers)
    
    context={'userprofile':userprofile,'fromusers':fromusers,'allotherprofiles':allotherprofiles}|notidict
    return render(request,'dms.html',context)

@login_required
def dmusersearch(request):
    # return HttpResponse('dm user search')
    dmsearch=None
    if request.method=="POST":
        dmsearch=request.POST.get('dmsearch')
    # print(dmsearch)
    return redirect(f'/dms/{dmsearch}')

@login_required
def dm(request,slug):
    # return HttpResponse(f'dm - {slug}')
    userprofile=Profile.objects.get(user=request.user)
    if User.objects.get(username=slug)==request.user:
        return redirect('dms')
    notifics=list(notifications(request.user))
    for n in notifics:
        if n.nfromuser==User.objects.get(username=slug) and n.ntype==92:
            notifics.remove(n)
            n.delete()
    # print(notifics)
    notidict={'notifics':notifics}
    try:
        touserprofile=Profile.objects.get(user=User.objects.get(username=slug))
    except Exception as e:
        return redirect('/dms')
    # print(touserprofile)
    dmsfromtouser=Dm.objects.filter(touser=request.user,fromuser=User.objects.get(username=slug),parent=None)
    dmstofromuser=Dm.objects.filter(fromuser=request.user,touser=User.objects.get(username=slug),parent=None)
    # print(dmsfromtouser,dmstofromuser)
    alldms=sorted(chain(dmsfromtouser,dmstofromuser),key=lambda x:x.timestamp)
    # print(alldms)
    repliesfromtouser=Dm.objects.filter(touser=request.user,fromuser=User.objects.get(username=slug)).exclude(parent=None)
    repliestofromuser=Dm.objects.filter(fromuser=request.user,touser=User.objects.get(username=slug)).exclude(parent=None)
    # print(repliesfromtouser,repliestofromuser)
    allreplies=sorted(chain(repliestofromuser,repliesfromtouser),key=lambda x:x.timestamp)
    # print(allreplies)
    repdict={}
    for reply in allreplies:
        if reply.parent.sno not in repdict.keys():
            repdict[reply.parent.sno]=[reply]
        else:
            repdict[reply.parent.sno].append(reply)
    # print(repdict)
    touser=User.objects.get(username=slug)
    context={'userprofile':userprofile,'slug':slug,'alldms':alldms,'touserprofile':touserprofile,'repdict':repdict}|notidict
    return render(request,'dm.html',context)
    
@login_required
def postdm(request):
    # return HttpResponse('posting dm')
    userprofile=Profile.objects.get(user=request.user)
    if request.method=='POST':
        chat=request.POST.get('chat')
        parentsno=request.POST.get('parentsno')
        fromuser=request.POST.get('fromuser')
        touser=request.POST.get('touser')
        fromuser=User.objects.get(username=fromuser)
        touser=User.objects.get(username=touser)
        # print(fromuser,type(fromuser))
        # print(touser,type(touser))
        if parentsno=="":
            dm=Dm(dmtext=chat,fromuser=fromuser,touser=touser,fpfp=userprofile)
            newnotif=Notification.objects.create(nfromuser=fromuser,ntouser=touser,ntype=92)
            newnotif.save()
            dm.save()
            messages.success(request,'message sent.')
        else:
            parent=Dm.objects.get(sno=parentsno)
            dm=Dm(dmtext=chat,fromuser=fromuser,touser=touser,fpfp=userprofile,parent=parent)
            newnotif=Notification.objects.create(nfromuser=fromuser,ntouser=touser,ntype=92)
            newnotif.save()
            dm.save()
            messages.success(request,'reply sent.')
    return redirect(f'/dms/{touser.username}#sendbtn')

@login_required
def postcomment(request):
    # return HttpResponse('post comment')
    if request.method=='POST':
        comment=request.POST.get('comment')
        user=request.user
        postid=request.POST.get('postid')
        postid=Post.objects.get(id=postid)
        pc=Postcomment(postid=postid,comment=comment,user=user)
        # print(pc)
        pc.save()
        messages.success(request,'comment posted.')
    return redirect(f'/#post{postid}')

@login_required
def predict(request,slug):
    # return HttpResponse(f'predict-{slug}')
    userprofile=Profile.objects.get(user=request.user)
    try:
        predictions=Predictmatch.objects.get(user1=request.user,user2=User.objects.get(username=slug))
        user1profile=Profile.objects.get(user=request.user)
        user2profile=Profile.objects.get(user=User.objects.get(username=slug))
    except:
        return redirect('/')
    # print(predictions)
    notifics=notifications(request.user)
    notidict={'notifics':notifics}
    context={'userprofile':userprofile,'predictions':predictions,'user1profile':user1profile,'user2profile':user2profile,'sportdict':{50: 'None', 51: 'Football', 52: 'Hockey', 53: 'Cricket', 54: 'Basketball', 55: 'Rugby', 56: 'Volleyball', 57: 'Prefer Video Games', 58: 'Badminton', 59: 'Tennis', 599: 'Table Tennis'},'hobbydict':{80: 'None', 81: 'Dancing', 82: 'Singing', 83: 'Acting', 84: 'Reading', 85: 'Drawing', 86: 'Writing', 87: 'Swimming'},'genderdict':{-1: 'Prefer not to disclose', 0: 'Female', 1: 'Male'}}|notidict
    return render(request,'predict.html',context)

@login_required
def postdelete(request):
    # return HttpResponse('delete post')
    return redirect(f'/profile/{request.user.username}')
    
@login_required
def dmdelete(request):
    # return HttpResponse('delete message')
    if request.method=='POST':
        dmsno=request.POST.get('dmsno')
        # print(dmsno)
        dm=Dm.objects.get(sno=dmsno)
        # print(dm)
        dm.delete()
    return redirect('/')

@login_required
def piro(request):
    # return HttpResponse('piro register')
    userprofile=Profile.objects.get(user=request.user)
    notifics=notifications(request.user)
    notidict={'notifics':notifics}
    context={'userprofile':userprofile}|notidict
    return render(request,'piro.html',context)

@login_required
def pirocreate(request):
    # return HttpResponse('create a piro user')
    if request.method=="POST":
        pirouser=request.POST.get('pirouser')
        type=request.POST.get('type')
        # print(pirouser,type)
        pu=Piro(user=User.objects.get(username=pirouser),type=type)
        pu.save()
    return redirect('piro')

def notifications(user):
    notifics=Notification.objects.filter(ntouser=user)
    # print(len(notifics))
    return notifics

@login_required
def notifdelete(request):
    # return HttpResponse('follow request delete notifications')
    if request.method=="POST":
        notifsno=request.POST.get('notifsno')
        # print(notifsno)
        notif=Notification.objects.get(sno=notifsno)
        # print(notif)
        followreq=Follow.objects.get(follower=notif.nfromuser,user=notif.ntouser,requested=True)
        # print(followreq)
        notif.delete()
        followreq.delete()
    return redirect('/')

@login_required
def notifaccept(request):
    # return HttpResponse('follow request accept notification')
    if request.method=="POST":
        anotifsno=request.POST.get('anotifsno')
        # print(notifsno)
        notif=Notification.objects.get(sno=anotifsno)
        # print(notif)
        followreq=Follow.objects.get(follower=notif.nfromuser,user=notif.ntouser,requested=True)
        followreq.requested=False
        # print(followreq)
        notif.delete()
        followreq.save()
    return redirect('/')
    
@login_required
def networkgraphcreate(request,sno):
    # return HttpResponse('create network graph ')
    userprofile=Profile.objects.get(user=request.user)
    try:
        graph=Networkgraph.objects.get(sno=sno)
        # print(graph)
    except:
        return redirect('/')
    notifics=notifications(request.user)
    notidict={'notifics':notifics}
    
    context={'userprofile':userprofile,'sno':sno,'graph':graph}|notidict
    return render(request,'netgraphdisplay.html',context)
    # plt.show()
    
    
    