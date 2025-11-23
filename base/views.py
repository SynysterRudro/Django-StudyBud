from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.db.models import Q
# Q is for complex queries adding and or operations
from .models import Room,Topic, Message
from .forms import RoomForm

# Create your views here.

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


#  
 

def loginPage(request):

     page = 'login'
     if request.user.is_authenticated:
          return redirect('home')


     if request.method == 'POST':
          username = request.POST.get('username') .lower()
          password = request.POST.get('password')

          try:
               user = User.objects.get(username=username)
          except:
               # print("User does not exist") 
               messages.error(request, 'User does not exist')
          user = authenticate(request, username=username, password=password)
          if user is not None:
               login(request, user)
               return redirect('home')
          else:
               messages.error(request, 'Username OR password does not exist')

     context = {'page': page }
     return render(request, 'base/login_register.html',context)


def logoutUser(request):
     logout(request)
     return redirect('home')

def registerPage(request):
     #  page = 'register'
      form = UserCreationForm()

      if request.method == 'POST':
           form = UserCreationForm(request.POST)
           if form.is_valid():
                user = form.save(commit=False)
                user.username = user.username.lower()
                user.save()
                login(request, user)  
                return redirect('home')
           else:
                messages.error(request, 'An error occurred during registration')
      return render(request, 'base/login_register.html', {'form': form} )


def home(request):
     # return HttpResponse("Home Page")

     q = request.GET.get('q') if request.GET.get('q') != None else ''
     rooms = Room.objects.filter(Q(topic__name__icontains= q) | 
                                  Q(name__icontains = q ) |
                                  Q(description__icontains = q )|
                                  Q(host__username__icontains=q)
                                  )
     topics = Topic.objects.all()
     room_count = rooms.count()
     context = {'rooms': rooms, 'topics': topics, 'room_count': room_count }
     return render(request, 'base/home.html', context)

def room(request,pk):
     # return HttpResponse("Room Page") 
     room = Room.objects.get(id=pk) 
     room_messages = room.message_set.all().order_by('-created')
     participants = room.participants.all()
     if request.method == 'POST':
          message = Message.objects.create(
               user=request.user,
               room=room,
               body=request.POST.get('body')
          )
          room.participants.add(request.user)
          return redirect('room', pk=room.id)
     # for i in rooms:
     #       if i['id'] == int(pk):
     #            room = i
     context = {'room': room, 'room_messages': room_messages, 'participants': participants} 



     return render(request, 'base/room.html',context)


# the line says only logged in users can access this view
@login_required(login_url='login')
def createRoom(request):
     form = RoomForm()
     if request.method == 'POST':
          form = RoomForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('home')

     context ={'form':form}
     return render(request,'base/room_form.html',context) 

@login_required(login_url='login')
def update_Room(request, pk):
    room = Room.objects.get(id=pk)  # Define 'room' first

    form = RoomForm(instance=room)

    if request.user != room.host:
            return HttpResponse("You are not allowed here!!")

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form} 
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def delete_Room(request, pk):
     room = Room.objects.get(id=pk) 

     if request.user != room.host:
          return HttpResponse("You are not allowed here!!")

     if request.method == 'POST':
          room.delete()
          return redirect('home')
     return render(request, 'base/delete.html',{'obj': room})



@login_required(login_url='login')
def delete_Message (request, pk):
     message = Message.objects.get(id=pk) 

     if request.user != message.user:
          return HttpResponse("You are not allowed here!!")

     if request.method == 'POST':
          message .delete()
          return redirect('home')
     return render(request, 'base/delete.html',{'obj': message })
