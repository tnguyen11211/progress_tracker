from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from PIL import Image

def getRecentDates(model, profile):
    if timezone.now().month <= 3:
        dates = model.objects.filter(date__month__range=['01', '03'], date__year=timezone.now().year, profile=profile)
    elif timezone.now().month > 3 and timezone.now().month <= 6:
        dates = model.objects.filter(date__month__range=['04', '06'], date__year=timezone.now().year, profile=profile)
    elif timezone.now().month > 6 and timezone.now().month <= 9:
        dates = model.objects.filter(date__month__range=['07', '09'], date__year=timezone.now().year, profile=profile)
    elif timezone.now().month > 9 and timezone.now().month <= 12:
        dates = model.objects.filter(date__month__range=['10', '12'], date__year=timezone.now().year, profile=profile)
    else:
        dates = model.objects.filter(profile=profile)

    return dates

class Profile(models.Model):
    BROWN = 'Brown'
    SR_BROWN = 'Sr. Brown'
    RED = 'Red'
    SR_RED = 'Sr. Red'
    BLACK1 = '1st Dan Black Belt'
    BLACK2 = '2nd Dan Black Belt'
    BLACK3 = '3rd Dan Black Belt'
    BLACK4 = '4th Dan Black Belt'
    BLACK5 = '5th Dan Black Belt'

    BELT_RANKS = (
        (BROWN,'Brown'),
        (SR_BROWN,'Sr. Brown'),
        (RED,'Red'),
        (SR_RED, 'Sr. Red'),
        (BLACK1,'1st Dan Black Belt'),
        (BLACK2,'2nd Dan Black Belt'),
        (BLACK3,'3rd Dan Black Belt'),
        (BLACK4,'4th Dan Black Belt'),
        (BLACK5,'5th Dan Black Belt')
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30, null=True)
    about = models.TextField(null=True, blank=True)
    picture = models.ImageField(default="default.svg", upload_to='profile_pictures', null=True)
    rank = models.CharField(max_length=20, choices=BELT_RANKS, null=True, blank=True)
    last_promoted = models.DateField(default=timezone.now)

    @property
    def current_attendances(self):
        return getRecentDates(Attendance, self).count()
    
    @property
    def current_tournaments(self):
        return getRecentDates(Tournament, self).count()
    
    @property
    def current_leadership_hours(self):
        leadership_hours = getRecentDates(LeadershipHours, self)
        current_hours = 0
        for h in leadership_hours:
            current_hours += h.hours
        return current_hours
    
    @property
    def current_practical_score(self):
        practical_scores =  getRecentDates(PracticalScore, self)
        if not practical_scores:
            return 0
        else:
            return practical_scores.first().score
        
    def get_recent_attendances(self):
        return getRecentDates(Attendance, self)
    
    def get_recent_tournaments(self):
        return getRecentDates(Tournament, self)
    
    def get_recent_leadership_hours(self):
        return getRecentDates(LeadershipHours, self)
    
    def get_recent_practical_scores(self):
        return getRecentDates(PracticalScore, self)

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
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='attendance')
    date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return self.__class__.__name__ + " for " + self.profile.name + " on " + self.date.strftime("%b %d, %Y")
    
    class Meta:
        ordering = ['-date']

class Tournament(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='tournament')
    event = models.CharField(max_length=30, null=True)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.__class__.__name__ + " for " + self.profile.name + " for " + self.event + " on " + self.date.strftime("%b %d, %Y")
    
    class Meta:
        ordering = ['-date', 'event']
    
class LeadershipHours(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='leadership_hour')
    event = models.CharField(max_length=30)
    date = models.DateField(default=timezone.now)
    hours = models.IntegerField(null=True)

    def __str__(self):
        string = self.__class__.__name__ + " for " + self.profile.name + " for " + self.event + " on " + self.date.strftime("%b %d, %Y") + " for " + str(self.hours) + " hours "
        return string

class PracticalScore(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='practical_score')
    date = models.DateField(default=timezone.now)
    score = models.IntegerField(null=True)

    def __str__(self):
        string = self.__class__.__name__ + " for " + self.profile.name + " on " + self.date.strftime("%b %d, %Y") + " with score " + str(self.score)
        return string
    
    class Meta:
        ordering = ['-date']

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