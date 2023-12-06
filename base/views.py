from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RoomForm, UserForm, ProfileForm
from .models import Message, Room, Topic, Profile, Tournament, LeadershipHours, PracticalScore

def getRecentDates(model):
    if timezone.now().month <= 3:
        dates = model.filter(date__month__range=['01', '03'], date__year=timezone.now().year)
    elif timezone.now().month > 3 and timezone.now().month <= 6:
        dates = model.filter(date__month__range=['04', '06'], date__year=timezone.now().year)
    elif timezone.now().month > 6 and timezone.now().month <= 9:
        dates = model.filter(date__month__range=['07', '09'], date__year=timezone.now().year)
    elif timezone.now().month > 9 and timezone.now().month <= 12:
        dates = model.filter(date__month__range=['10', '12'], date__year=timezone.now().year)
    else:
        dates = model.all()

    return dates

def setProfileStats():
    profiles = Profile.objects.all()
    tournaments = getRecentDates(Tournament.objects)
    hours = getRecentDates(LeadershipHours.objects)
    practicals = getRecentDates(PracticalScore.objects)

    for profile in profiles:
        profile.current_attendances = getRecentDates(profile.attendances).count()

        tournament_count = 0
        for tournament in tournaments:
            if profile == tournament.profile:
                tournament_count += 1
        profile.current_tournaments = tournament_count

        hours_count = 0
        for h in hours:
            if profile == h.profile:
                hours_count += h.hours
        profile.current_hours = hours_count

        for practical in practicals:
            if profile == practical.profile:
                profile.current_score = practical.score

        profile.save()

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    profiles = Profile.objects.filter(
        Q(user__username__icontains=q) |
        Q(name__icontains=q)
    )
        
    context = {'profiles': profiles}
    return render(request, 'base/home.html', context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
    page = 'register'
    form = UserCreationForm()
    context = {'page': page, 'form': form}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # change or clean form data here
            user.save()
            user.profile.name = user.username
            user.save()
            login(request, user)
            return redirect('home')
        else:
            for error in form.errors:
                messages.error(request, form.errors.get(error))

    return render(request, 'base/login_register.html', context)


def rooms(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count_all = Room.objects.all().count()
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q) | 
        Q(room__name__icontains=q) |
        Q(room__description__icontains=q)
        )[0:5]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_count_all': room_count_all, 'room_messages': room_messages}
    return render(request, 'base/rooms.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('updated', 'created')
    participants = room.participants.all()
    if request.method == 'POST':
        Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        if not room.participants.contains(request.user):
            room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    profile = user.profile
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    room_count_all = Room.objects.all().count()
    topics = Topic.objects.all()

    attendances = profile.attendances.all()
    tournaments = Tournament.objects.filter(profile=profile)
    hours = LeadershipHours.objects.filter(profile=profile)
    practical_scores = PracticalScore.objects.filter(profile=profile)

    context = {'user': user,
               'rooms': rooms,
               'room_messages': room_messages, 
               'room_count_all': room_count_all, 
               'topics': topics,
               'attendances': attendances,
               'tournaments': tournaments,
               'hours': hours,
               'practical_scores': practical_scores
               }
    
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    create_update = "Create"

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('rooms')

    context = {'form': form, 'topics': topics, 'create_update': create_update}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    create_update = "Update"

    if request.user != room.host:
        return HttpResponse('Invalid operation. Users can only edit rooms they have created.')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', room.id)

    context = {'form': form, 'topics': topics,
               'room': room, 'create_update': create_update}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Invalid operation. Users can only delete rooms they have created.')

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Invalid operation. Users can only delete messages they have created.')

    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    user_form = UserForm(instance=user)
    profile_form = ProfileForm(instance=user.profile)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            setProfileStats()
            return redirect('user-profile', pk=user.id)
        else:
            for error in user_form.errors:
                messages.error(request, user_form.errors.get(error))
            for error in profile_form.errors:
                messages.error(request, profile_form.errors.get(error))

    return render(request, 'base/update-user.html', {'user_form': user_form, 'profile_form': profile_form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(Q(name__icontains=q))
    rooms = Room.objects.all()

    return render(request, 'base/topics.html', {'topics': topics, 'rooms': rooms})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
