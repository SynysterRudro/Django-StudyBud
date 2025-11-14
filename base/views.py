from django.shortcuts import render, redirect 
from .models import Room,Topic
from .forms import RoomForm

# Create your views here.

from django.http import HttpResponse


#  

def home(request):
     # return HttpResponse("Home Page")

     rooms = Room.objects.all()
     topics = Topic.objects.all()
     context = {'rooms': rooms, 'topics': topics}
     return render(request, 'base/home.html', context)

def room(request,pk):
     # return HttpResponse("Room Page") 
     room = Room.objects.get(id=pk) 
     # for i in rooms:
     #       if i['id'] == int(pk):
     #            room = i
     context = {'room': room} 



     return render(request, 'base/room.html',context)

def createRoom(request):
     form = RoomForm()
     if request.method == 'POST':
          form = RoomForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('home')

     context ={'form':form}
     return render(request,'base/room_form.html',context) 

def update_Room(request, pk):
    room = Room.objects.get(id=pk)  # Define 'room' first

    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form} 
    return render(request, 'base/room_form.html', context)

def delete_Room(request, pk):
     room = Room.objects.get(id=pk)     
     if request.method == 'POST':
          room.delete()
          return redirect('home')
     return render(request, 'base/delete.html',{'obj': room})



