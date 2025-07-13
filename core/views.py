from django.db.models import Count
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from core.filters import LessonFilter
from core.models import Lesson, Response as SavedResponse
from core.serializers import LessonModelSerializer
from rag.qa import answer_question


# Create your views here.

# upload content API View
# GET and POST
class UploadContentView(APIView):
    # to upload the content to db
    def post(self, request):
        serializer = LessonModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Content uploaded successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # to retrieve tha uploaded content from db
    def get(self, request):
        queryset = Lesson.objects.all()
        serializer = LessonModelSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# API to ask question
# which retrieves the answer from model
class AskView(APIView):
    def post(self, request):
        question = request.data.get("question")
        persona = request.data.get("persona", "friendly")
        if not question:
            return Response({"error": "Missing question."}, status=status.HTTP_400_BAD_REQUEST)
        answer = answer_question(question, persona)
        SavedResponse.objects.create(question=question, answer=answer)
        return Response(answer, status=status.HTTP_200_OK)


# Render the frontend to ask questions
def index(request):
    return render(request, "index.html")


# API to list all the saved response from the model
class SavedResponseView(APIView):
    def get(self, request):
        queryset = SavedResponse.objects.all()
        serializer = LessonModelSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# List/retrieve/filter uploaded data
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonModelSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LessonFilter


# API for general overview
class MetricsView(APIView):
    def get(self, request):
        total_lessons = Lesson.objects.count()
        unique_topics = Lesson.objects.values("topic").distinct().count()
        files_uploaded = Lesson.objects.exclude(content="").count()

        lessons_per_grade = Lesson.objects.values("grade").annotate(count=Count("id"))
        lessons_per_grade_dict = {item["grade"]: item["count"] for item in lessons_per_grade}

        return Response({
            "total_lessons": total_lessons,
            "unique_topics": unique_topics,
            "files_uploaded": files_uploaded,
            "lessons_per_grade": lessons_per_grade_dict,
        })
