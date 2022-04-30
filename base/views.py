from multiprocessing import context
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm

'''
rooms=[
    {'id':1, 'name':'C++'},
    {'id':2, 'name':'Java'},
    {'id':3, 'name':'GoLang'},
    {'id':4, 'name':'Scala'},
]
'''
# Create your views here.
def Home(request):
    rooms=Room.objects.all()
    context={'rooms':rooms}
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