from rest_framework import serializers

from core.models import Lesson, Response


class LessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "title",
            "topic",
            "grade",
            "content",
        ]


class SavedResponseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Response
        fields = [
            "question",
            "answer"
        ]
