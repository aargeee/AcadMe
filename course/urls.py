from django.urls import path
from .views import (
    CourseView,
    CourseDetailView,
    SearchAndFilterView,
    CategoryListCreateView,
    CategoryManageView,
    ContentView,
)

urlpatterns = [
    path("", CourseView.as_view(), name="course-list"),
    path("search/", SearchAndFilterView.as_view(), name="search"),
    path("<uuid:courseid>/content/", CourseDetailView.as_view(), name="course-manage"),
    path("category/", CategoryListCreateView.as_view(), name="category-list"),
    path(
        "category/<uuid:categoryid>/",
        CategoryManageView.as_view(),
        name="category-manage",
    ),
    path("content/<uuid:contentid>/", ContentView.as_view(), name="content-view"),
]
