import uuid

from django.db import models


class Lesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    topic = models.CharField(max_length=255)
    grade = models.CharField(max_length=20)
    content = models.TextField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"{self.title} - Grade {self.grade}"


class Response(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.TextField()
    answer = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return f"{self.question}"
