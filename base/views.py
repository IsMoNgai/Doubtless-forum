from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Questions, Topic, Answer, User
from .forms import QuestionsForm, UserForm, MyUserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
# we can place all our page functions here for good prac

#quests = [
#    {"id": 1, "name" : "physics"},
#    {"id": 2, "name" : "math"},
#    {"id": 3, "name" : "chinese"},
#]

def loginPage(request):
    page = 'login'
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username OR password does not exist")


    context = {'page': page}
    return render(request, 'login_registration.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower() #require username to be lowercase
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error occured during registration.")

    return render(request, 'login_registration.html', {'form':form})

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    quests = Questions.objects.filter(Q(topic__name__contains=q) | 
                                      Q(name__contains=q) |
                                      Q(description__contains=q))

    topic = Topic.objects.all()[0:5]
    questions_count = quests.count()
    questions_answers = Answer.objects.filter(Q(quest__topic__name__icontains=q))

    context = {"quests" : quests, "topics" : topic, "questions_count":questions_count, "questions_answers": questions_answers}
    return render(request, 'home.html', context)

def rules(request):
    return render(request, 'rules.html')

def questions(request, pk):
    quest = Questions.objects.get(id=pk)
    answer_messages = quest.answer_set.all()
    participants = quest.participants.all()
    if request.method == "POST":
        message = Answer.objects.create(
            user = request.user,
            quest = quest,
            body = request.POST.get('body')
        )
        quest.participants.add(request.user)
        return redirect('questions', pk=quest.id)
  
    context = {'quest': quest, 'answer_messages':answer_messages, 'participants':participants }
    return render(request, 'questions.html', context)

def userProfile(request, pk):
    user = User.objects.get(id = pk)
    quests = user.questions_set.all()
    questions_answers = user.answer_set.all()
    topics = Topic.objects.all()
    context={'user':user, 'quests':quests, 'questions_answers':questions_answers, 'topics': topics}
    return render(request, 'profile.html', context)

@login_required(login_url="login")
def createQuestions(request):
    form = QuestionsForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        form = QuestionsForm(request.POST)

        Questions.objects.create(
            host=request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
        )
        return redirect('home')

    context = {'form':form, 'topics':topics}
    return render(request, 'Questions_form.html', context)

@login_required(login_url="login")
def updateQuestions(request, pk):
    quest = Questions.objects.get(id=pk)
    form = QuestionsForm(instance=quest)
    topics = Topic.objects.all()

    if request.user != quest.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        quest.name = request.POST.get('name')
        quest.topic = topic
        quest.description = request.POST.get('description')
        quest.save()
        return redirect('home')        

    context = {'form':form, 'topics':topics, 'quest':quest}
    return render(request, 'Questions_form.html', context)

@login_required(login_url="login")
def deleteQuestions(request, pk):
    quest = Questions.objects.get(id=pk)

    if request.user != quest.host:
        return HttpResponse('You are not allowed here!!!')

    if request.method == "POST":
        quest.delete()
        return redirect('user-profile', pk=request.user.id)

    return render(request, 'delete.html', {'obj':quest})

@login_required(login_url="login")
def deleteAnswer(request, pk):
    answer = Answer.objects.get(id=pk)

    if request.user != answer.user:
        return HttpResponse("You are not allowed here!!!")

    if request.method == "POST":
        answer.delete()
        return redirect('user-profile', pk=request.user.id)

    return render(request, 'delete.html', {'obj':answer})

@login_required(login_url="login")
def UpdateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form':form}
    return render(request, 'update-user.html', context)


def TopicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    topics = Topic.objects.filter(name__icontains=q)

    return render(request, 'topics.html', {'topics':topics})

def ActivityPage(request):

    questions_answers = Answer.objects.all()[0:3]

    return render(request, 'activity.html', {'questions_answers':questions_answers})