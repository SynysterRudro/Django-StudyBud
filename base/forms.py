
from django.forms import ModelForm
from .models import Room



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        # fields = ['name', 'description']  # you can also specify fields individuallyß 
        exclude = ['host', 'participants']  # you can also exclude fields individually