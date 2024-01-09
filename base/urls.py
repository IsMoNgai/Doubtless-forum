from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),

    path('', views.home, name="home"),
    path('rules/', views.rules, name="rules"),
    path('questions/<str:pk>/', views.questions, name="questions"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
   
    path('create-questions/', views.createQuestions, name="create-questions"),
    path('update-questions/<str:pk>/', views.updateQuestions, name="update-questions"),
    path('delete-questions/<str:pk>/', views.deleteQuestions, name="delete-questions"),
    path('delete-answer/<str:pk>/', views.deleteAnswer, name="delete-answer"),

    path('update-user/', views.UpdateUser, name="update-user"),
    
    path('topics/', views.TopicsPage, name="topics"),
    path('activity/', views.ActivityPage, name="activity"),
]