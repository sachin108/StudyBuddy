from multiprocessing import context
from django.contrib import messages
from django.shortcuts import redirect, render
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
from django.contrib.auth.models import User
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

    context={}
    return render(request, 'base/login_register.html', context)

def Home(request):
    q=request.GET.get('q') 
    rooms=Room.objects.all( )
    room_count=rooms.count()
    topics=Topic.objects.all()
    context={'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render(request, 'base/home.html', context)

def room(request, pk):
    room=Room.objects.get(id=pk)
    context={'room':room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form=RoomForm()
    if(request.method=='POST'):
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')

    context={'form':form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room=Room.objects.get(id=pk)
    form=RoomForm(instance=room)
    
    if request.method=='POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')
    
    context={ 'form':form }
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room=Room.objects.get(id=pk)
    if request.method=='POST':
        room.delete()
        return redirect('Home')
    
    return render(request, 'base/delete.html', {'obj':room})