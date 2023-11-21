from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Room, Profile

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['picture', 'name', 'rank', 'about']