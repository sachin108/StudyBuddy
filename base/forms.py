import imp
from pyexpat import model
from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):
    class Meta:
        fields = '__all__'
        model = Room 
        exclude=['host', 'participants']