from django.urls import path
from .views import CourseView, CourseDetailView

urlpatterns = [
    path("", CourseView.as_view(), name="course-list"),
    path("<uuid:courseid>/content", CourseDetailView.as_view(), name="course-manage"),
    # path("search/", )
]
