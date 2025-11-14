from django.contrib import admin

# Register your models here.


from .models import Room, Topic, Message

# we need to register the Room model so that it appears in the admin panel
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)  
