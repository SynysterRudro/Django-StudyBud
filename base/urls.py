from django.urls import path

from . import views

urlpatterns = [

    path('login/', views.loginPage, name='login'),
    path('', views.home, name='home'),
    path('room/<str:pk>', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<str:pk>', views.update_Room, name='update-room'),
    path('delete-room/<str:pk>', views.delete_Room, name='delete-room'),
    
] 
