from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    BELT_RANKS = (
        ('brown','Brown'),
        ('sr_brown','Sr. Brown'),
        ('red','Red'),
        ('sr_red', 'Sr. Red'),
        ('black_1','1st Dan Black Belt'),
        ('black_2','2nd Dan Black Belt'),
        ('black_3','3rd Dan Black Belt'),
        ('black_4','4th Dan Black Belt'),
        ('black_5','5th Dan Black Belt'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, null=True)
    about = models.TextField(null=True)
    picture = models.ImageField(default="default.svg", upload_to='profile_pictures', null=True)
    rank = models.CharField(max_length=20, choices=BELT_RANKS, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}\'s Profile'
    
    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        if not self.picture.url.endswith('.svg'):
            img = Image.open(self.picture.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                # create a thumbnail
                img.thumbnail(output_size)
                # overwrite the larger image
                img.save(self.picture.path)

class Attendance(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=datetime.today())

    def __str__(self):
        return self.date.strftime("%b %d, %Y")

class Tournament(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True)
    date = models.DateField(default=datetime.today())
    
    def __str__(self):
        return self.name

class TeachingHours(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=datetime.today())
    hours = models.IntegerField(null=True)

    def __str__(self):
        string = self.date.strftime("%b %d, %Y") + " : " + str(self.hours)
        return string

class ServiceHours(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    event = models.CharField(max_length=200)
    date = models.DateField(default=datetime.today())
    hours = models.IntegerField(null=True)

    def __str__(self):
        string = self.event + " : " + self.date.strftime("%b %d, %Y") + " : " + str(self.hours)
        return string
    
class PracticalScore(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=datetime.today())
    score = models.IntegerField(null=True)

    def __str__(self):
        string = self.date.strftime("%b %d, %Y") + " : " + str(self.score)
        return string

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]