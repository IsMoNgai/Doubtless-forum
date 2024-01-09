from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Questions
from .serializers import QuestionsSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/questions', 
        'GET /api/questions/:id'
    ]

    return Response(routes)

#get a list of questions
@api_view(['GET'])
def getQuestions(request):
    quests= Questions.objects.all()
    serializer = QuestionsSerializer(quests, many=True)
    return Response(serializer.data)

#get a single question
@api_view(['GET'])
def getQuestion(request, pk):
    quests= Questions.objects.get(id=pk)
    serializer = QuestionsSerializer(quests, many=False)
    return Response(serializer.data)