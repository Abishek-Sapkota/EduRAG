from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AskView, UploadContentView, index, MetricsView, LessonViewSet, SavedResponseView

router = DefaultRouter()
router.register(r"topic", LessonViewSet, basename="lesson")


urlpatterns = [
    path("", index, name="index"),
    path("", include(router.urls)),
    path("upload-content/", UploadContentView.as_view()),
    path("ask/", AskView.as_view()),
    path("saved-response/", SavedResponseView.as_view()),
    path("metrics/", MetricsView.as_view()),
]
