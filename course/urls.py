from django.urls import path
from .views import (
    CourseView,
    CourseDetailView,
    SearchAndFilterView,
    CategoryListCreateView,
    CategoryManageView,
    ContentView,
    LearnerEnrollView,
    ContentMarkCompleteView,
)

urlpatterns = [
    path("", CourseView.as_view(), name="course-list"),
    path("search/", SearchAndFilterView.as_view(), name="search"),
    path("<uuid:courseid>/content/", CourseDetailView.as_view(), name="course-manage"),
    path("<uuid:courseid>/enroll/", LearnerEnrollView.as_view(), name="course-enroll"),
    path("category/", CategoryListCreateView.as_view(), name="category-list"),
    path(
        "category/<uuid:categoryid>/",
        CategoryManageView.as_view(),
        name="category-manage",
    ),
    path("content/<uuid:contentid>/", ContentView.as_view(), name="content-view"),
    path("content/<uuid:contentid>/markcomplete", ContentMarkCompleteView.as_view(), name="content-mark-complete"),
]
