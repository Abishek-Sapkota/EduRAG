from django_filters import FilterSet

from core.models import Lesson


class LessonFilter(FilterSet):
    class Meta:
        model = Lesson
        fields = {
            "topic": ["exact", "icontains", "iexact"],
            "title": ["exact", "icontains", "iexact"],
            "content": ["exact", "icontains", "iexact"],
            "grade": ["exact"],
        }
