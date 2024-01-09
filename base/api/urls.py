from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('quests/', views.getQuestions),
    path('quests/<str:pk>', views.getQuestion)
]