from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RoomForm, UserForm, ProfileForm, AttendanceForm, TournamentForm, LeadershipHoursForm, PracticalScoreForm
from .models import Attendance, Tournament, LeadershipHours, PracticalScore, Message, Room, Topic, Profile

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    profiles = Profile.objects.filter(
        Q(user__username__icontains=q) |
        Q(name__icontains=q)
    )

    time = timezone.localdate

    context = {'profiles': profiles, 'time': time}
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
            login(request, user)
            return redirect('home')
        else:
            for error in form.errors:
                messages.error(request, form.errors.get(error))

    return render(request, 'base/login_register.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    profile = user.profile

    attendances = profile.get_recent_attendances()[:5]
    tournaments = profile.get_recent_tournaments()[:5]
    leadership_hours = profile.get_recent_leadership_hours()[:5]
    practical_scores = profile.get_recent_practical_scores()[:5]

    context = {'user': user, 
               'attendances': attendances,
               'tournaments': tournaments,
               'leadership_hours': leadership_hours,
               'practical_scores': practical_scores}
    
    return render(request, 'base/profile.html', context)

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
            return redirect('user-profile', pk=user.id)
        else:
            for error in user_form.errors:
                messages.error(request, user_form.errors.get(error))
            for error in profile_form.errors:
                messages.error(request, profile_form.errors.get(error))

    return render(request, 'base/update-user.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required(login_url='login')
def createAttendance(request):
    profile = request.user.profile
    form = AttendanceForm()
    create_update = "Create"

    if request.method == 'POST':
        Attendance.objects.create(
            profile=profile,
            date=request.POST.get('date')
        )
        next = request.POST.get('next', '/')
        return redirect(next)

    context = {'form': form, 'create_update': create_update}
    return render(request, 'base/stats_form.html', context)

@login_required(login_url='login')
def updateAttendance(request, pk):
    attendance = Attendance.objects.get(id=pk)
    form = AttendanceForm(instance=attendance)
    create_update = "Update"

    if request.user != attendance.profile.user:
        return HttpResponse('Invalid operation. Users can only edit their own attendances.')

    if request.method == 'POST':
        attendance.date = request.POST.get('date')
        attendance.save()
        next = request.POST.get('next', '/')
        return redirect(next)

    context = {'form': form, 'create_update': create_update}
    return render(request, 'base/stats_form.html', context)

@login_required(login_url='login')
def deleteAttendance(request, pk):
    attendance = Attendance.objects.get(id=pk)

    if request.user != attendance.profile.user:
        return HttpResponse('Invalid operation. Users can only delete attendances they have created.')

    if request.method == 'POST':
        attendance.delete()
        next = request.POST.get('next', '/')
        return redirect(next)

    return render(request, 'base/delete.html', {'obj': attendance})

@login_required(login_url='login')
def createTournament(request):
    profile = request.user.profile
    form = TournamentForm()
    create_update = "Create"

    if request.method == 'POST':
        Tournament.objects.create(
            profile=profile,
            event=request.POST.get('event'),
            date=request.POST.get('date')
        )
        next = request.POST.get('next', '/')
        return redirect(next)

    context = {'form': form, 'create_update': create_update}
    return render(request, 'base/stats_form.html', context)

@login_required(login_url='login')
def updateTournament(request, pk):
    tournament = Tournament.objects.get(id=pk)
    form = TournamentForm(instance=tournament)
    create_update = "Update"

    if request.user != tournament.profile.user:
        return HttpResponse('Invalid operation. Users can only edit their own tournaments.')

    if request.method == 'POST':
        tournament.event = request.POST.get('event')
        tournament.date = request.POST.get('date')
        tournament.save()
        next = request.POST.get('next', '/')
        return redirect(next)

    context = {'form': form, 'create_update': create_update}
    return render(request, 'base/stats_form.html', context)

@login_required(login_url='login')
def deleteTournament(request, pk):
    tournament = Tournament.objects.get(id=pk)

    if request.user != tournament.profile.user:
        return HttpResponse('Invalid operation. Users can only delete tournaments they have created.')

    if request.method == 'POST':
        tournament.delete()
        next = request.POST.get('next', '/')
        return redirect(next)

    return render(request, 'base/delete.html', {'obj': tournament})

@login_required(login_url='login')
def createLeadershipHours(request):
    profile = request.user.profile
    form = LeadershipHoursForm()
    create_update = "Create"

    if request.method == 'POST':
        LeadershipHours.objects.create(
            profile=profile,
            event=request.POST.get('event'),
            date=request.POST.get('date'),
            hours=request.POST.get('hours')
        )
        next = request.POST.get('next', '/')
        return redirect(next)

    context = {'form': form, 'create_update': create_update}
    return render(request, 'base/stats_form.html', context)

@login_required(login_url='login')
def updateLeadershipHours(request, pk):
    leadership_hour = LeadershipHours.objects.get(id=pk)
    form = LeadershipHoursForm(instance=leadership_hour)
    create_update = "Update"

    if request.user != leadership_hour.profile.user:
        return HttpResponse('Invalid operation. Users can only edit their own leadership hours.')

    if request.method == 'POST':
        leadership_hour.event = request.POST.get('event')
        leadership_hour.date = request.POST.get('date')
        leadership_hour.hours = request.POST.get('hours')
        leadership_hour.save()
        next = request.POST.get('next', '/')
        return redirect(next)

    context = {'form': form, 'create_update': create_update}
    return render(request, 'base/stats_form.html', context)

@login_required(login_url='login')
def deleteLeadershipHours(request, pk):
    leadership_hour = LeadershipHours.objects.get(id=pk)

    if request.user != leadership_hour.profile.user:
        return HttpResponse('Invalid operation. Users can only delete leadership hours they have created.')

    if request.method == 'POST':
        leadership_hour.delete()
        next = request.POST.get('next', '/')
        return redirect(next)

    return render(request, 'base/delete.html', {'obj': leadership_hour})

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def createPracticalScore(request):
    profile = request.user.profile
    form = PracticalScoreForm()
    create_update = "Create"

    if request.method == 'POST':
        PracticalScore.objects.create(
            profile=profile,
            date=request.POST.get('date'),
            score=request.POST.get('score')
        )
        next = request.POST.get('next', '/')
        return redirect(next)

    context = {'form': form, 'create_update': create_update}
    return render(request, 'base/stats_form.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def updatePracticalScore(request, pk):
    practical_score = PracticalScore.objects.get(id=pk)
    form = PracticalScoreForm(instance=practical_score)
    create_update = "Update"

    if request.user != practical_score.profile.user:
        return HttpResponse('Invalid operation. Users can only edit their own practical scores.')

    if request.method == 'POST':
        practical_score.date = request.POST.get('date')
        practical_score.score = request.POST.get('score')
        practical_score.save()
        next = request.POST.get('next', '/')
        return redirect(next)

    context = {'form': form, 'create_update': create_update}
    return render(request, 'base/stats_form.html', context)

@login_required(login_url='login')
@user_passes_test(lambda u: u.is_superuser)
def deletePracticalScore(request, pk):
    practical_score = PracticalScore.objects.get(id=pk)

    if request.user != practical_score.profile.user:
        return HttpResponse('Invalid operation. Users can only delete practical scores they have created.')

    if request.method == 'POST':
        practical_score.delete()
        next = request.POST.get('next', '/')
        return redirect(next)

    return render(request, 'base/delete.html', {'obj': practical_score})

@login_required(login_url='login')
def statsPage(request, pk):
    profile = Profile.objects.get(id=pk)
    attendances = Attendance.objects.filter(profile=profile)
    tournaments = Tournament.objects.filter(profile=profile)
    hours = LeadershipHours.objects.filter(profile=profile)
    scores = PracticalScore.objects.filter(profile=profile)

    context = {
        'profile': profile,
        'attendances': attendances,
        'tournaments': tournaments,
        'hours': hours,
        'scores': scores
    }

    return render(request, 'base/stats.html', context)

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

def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(Q(name__icontains=q))
    rooms = Room.objects.all()

    return render(request, 'base/topics.html', {'topics': topics, 'rooms': rooms})

def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})
