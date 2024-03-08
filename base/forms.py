from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.utils import timezone

from .models import Room, Profile, Attendance, Tournament, LeadershipHours, PracticalScore

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
        fields = ['username', 'first_name', 'email']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['picture', 'rank', 'last_promoted', 'about']
        widgets = {
            'last_promoted': DateInput(attrs=dict(max = timezone.localdate)),
        }

class AttendanceForm(ModelForm):
    class Meta:
        model = Attendance
        fields = ['profile', 'date']
        widgets = {
            'date': DateInput(attrs=dict(max = timezone.localdate)),
        }

class TournamentForm(ModelForm):
    class Meta:
        model = Tournament
        fields = ['profile', 'event', 'date']
        widgets = {
            'date': DateInput(attrs=dict(max = timezone.localdate)),
        }

class LeadershipHoursForm(ModelForm):
    class Meta:
        model = LeadershipHours
        fields = ['profile', 'event', 'date', 'hours']
        widgets = {
            'date': DateInput(attrs=dict(max = timezone.localdate)),
        }

class PracticalScoreForm(ModelForm):
    class Meta:
        model = PracticalScore
        fields = ['profile', 'date', 'score']
        widgets = {
            'date': DateInput(attrs=dict(max = timezone.localdate)),
        }