from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('rooms/', views.rooms, name="rooms"),
    path('room/<str:pk>', views.room, name="room"),
    path('profile/<str:pk>', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),

    path('profile/<str:pk>/attendances/', views.statsPage, name="attendances"),
    path('profile/<str:pk>/create-attendance/', views.createAttendance, name="create-attendance"),
    path('update-attendance/<str:pk>/', views.updateAttendance, name="update-attendance"),
    path('delete-attendance/<str:pk>/', views.deleteAttendance, name="delete-attendance"),

    path('profile/<str:pk>/tournaments/', views.statsPage, name="tournaments"),
    path('profile/<str:pk>/create-tournament/', views.createTournament, name="create-tournament"),
    path('update-tournament/<str:pk>/', views.updateTournament, name="update-tournament"),
    path('delete-tournament/<str:pk>/', views.deleteTournament, name="delete-tournament"),

    path('profile/<str:pk>/leadership-hours/', views.statsPage, name="leadership-hours"),
    path('profile/<str:pk>/create-leadership-hours/', views.createLeadershipHours, name="create-leadership-hours"),
    path('update-leadership-hours/<str:pk>/', views.updateLeadershipHours, name="update-leadership-hours"),
    path('delete-leadership-hours/<str:pk>/', views.deleteLeadershipHours, name="delete-leadership-hours"),

    path('profile/<str:pk>/practical-scores/', views.statsPage, name="practical-scores"),
    path('profile/<str:pk>/create-practical-score/', views.createPracticalScore, name="create-practical-score"),
    path('update-practical-score/<str:pk>/', views.updatePracticalScore, name="update-practical-score"),
    path('delete-practical-score/<str:pk>/', views.deletePracticalScore, name="delete-practical-score"),
    
    path('update-user/<str:pk>/', views.updateUser, name="update-user"),

    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]