from email import message
from email.policy import default
from multiprocessing import context
from unicodedata import name
from venv import create
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from .models import Message, Room, Topic
from .forms import RoomForm, UserForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
'''
rooms=[
    {'id':1, 'name':'C++'},
    {'id':2, 'name':'Java'},
    {'id':3, 'name':'GoLang'},
    {'id':4, 'name':'Scala'},
]
'''
# Create your views here.


def loginPage(request):
    page='login'

    if request.user.is_authenticated:
        return redirect('Home')

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist!")

        user=authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, "username or password is incorrect!")

    context={'page':page}
    return render(request, 'base/login_register.html', context)

def registerPage(request):
    form=UserCreationForm()
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, "An error occurred during registeration")
    return render(request, 'base/login_register.html', {'form':form})

def logoutUser(request):
    logout(request)
    return redirect('Home')
    
def Home(request):
    q=request.GET.get('q', default="") 
    rooms=Room.objects.all()
    room_count=rooms.count()
    topics=Topic.objects.all()
    room_messages=Message.objects.filter(Q(room__topic__name__icontains=q))
    context={'rooms':rooms, 'topics':topics, 'room_count':room_count, "room_messages":room_messages}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')
    participants=room.participants.all()
    if request.method=='POST':
        message=Message.objects.create(
            user=request.user, 
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context={'room':room, 'room_messages':room_messages, "participants":participants}
    return render(request, 'base/room.html', context)

def userProfile(request, pk):
    user=User.objects.get(id=pk)
    rooms=user.room_set.all()
    room_messages=user.message_set.all()
    topics=Topic.objects.all()
    context={"user":user, "rooms":rooms, "room_messages":room_messages, "topics":topics}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')  #2h44m
def createRoom(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if(request.method=='POST'):
        topic_name=request.POST.get('topic')
        topic, created=Topic.objects.get_or_create(name=topic_name)
        form=RoomForm(request.POST)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            desccription=request.POST.get('desccription')
        )
        return redirect('Home')

    context={'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')  #2h44m
def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()

    if request.user != room.host:
        return HttpResponse("You're not allowed here!")
    
    if request.method=='POST':
        topic_name=request.POST.get('topic')
        topic, created=Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.desccription=request.POST.get('desccription')
        room.save()
        return redirect('Home')
    
    context={ 'form':form, 'topics':topics, 'room':room }
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')  #2h44m
def deleteRoom(request, pk):
    room=Room.objects.get(id=pk)

    if request.user !=  room.host:
        return HttpResponse("You are not allowed here!")

    if request.method=='POST':
        room.delete()
        return redirect('Home')
    
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')  #2h44m
def deleteMessage(request, pk):
    message=Message.objects.get(id=pk)

    if request.user !=  message.user:
        return HttpResponse("You are not allowed here!")

    if request.method=='POST':
        message.delete()
        return redirect('Home')
    
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')  #2h44m
def updataUser(request):
    user=request.user
    form=UserForm(instance=user)

    if request.method=='POST':
        form=UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form':form})