from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone

from .models import Room, Profile

class DateInput(forms.DateInput):
    input_type = 'date'

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
        fields = ['picture', 'name', 'rank', 'last_promoted', 'about']
        widgets = {
            'last_promoted': DateInput(attrs=dict(max = timezone.localdate)),
        }