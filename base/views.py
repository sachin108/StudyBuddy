from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse

rooms=[
    {'id':1, 'name':'C++'},
    {'id':2, 'name':'Java'},
    {'id':3, 'name':'GoLang'},
    {'id':4, 'name':'Scala'},
]

# Create your views here.
def Home(request):
    context={'rooms':rooms}
    return render(request, 'base/home.html', context)

def Room(request, pk):
    room=None
    for i in rooms:
        if i['id']==int(pk):
            room=i
        context={'room':room}
    return render(request, 'base/room.html', context)
