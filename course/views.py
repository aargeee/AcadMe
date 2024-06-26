# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotAuthenticated
from rest_framework.permissions import IsAuthenticated

from .models import Course, CourseTutor, Category, Content, Enrollment
from .serializers import (
    CourseSerializer,
    CourseDetailSerializer,
    CategorySerializer,
    ContentSerializer,
    ContentCompletionSerializer,
    ContentCompletionLogSerializer
)
from AcadMe.permissions import HasPermission

from django.shortcuts import get_object_or_404
from django.db.models import Q

from uuid import UUID
from .models import ContentCompletionLog


class CourseView(APIView):
    permission_classes = [HasPermission]
    permission_dict = {"POST": ["add_course"]}

    def get(self, _request: Request) -> Response:
        courseList = Course.objects.all()
        serialized = CourseSerializer(courseList, many=True)
        response = {"success": True, "data": serialized.data}
        return Response(data=response, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serialized = CourseSerializer(data=request.data)
        if not serialized.is_valid():
            raise ValidationError(detail=serialized.errors)
        course: Course = serialized.save(created_by=request.user)
        response = {"success": True, "data": {"course_id": course.id}}
        return Response(data=response, status=status.HTTP_201_CREATED)


class CourseDetailView(APIView):
    permission_classes = []

    def get(self, request: Request, courseid: UUID) -> Response:
        course = get_object_or_404(Course, id=courseid)
        serialized = CourseDetailSerializer(course)
        response = {"success": True, "data": serialized.data}
        return Response(data=response, status=status.HTTP_200_OK)
    
    def post(self, request: Request, courseid: UUID) -> Response:
        course = get_object_or_404(Course, id=courseid)
        logs = ContentCompletionLog.objects.filter(learner=request.user, content__chapter__course=course)
        enrolled = Enrollment.objects.filter(course=course, learner=request.user).exists()
        response = {"success": True, "data": {"content_id": logs.values_list('content_id', flat=True), "enrolled": enrolled}}
        return Response(data=response, status=status.HTTP_200_OK)


class SearchAndFilterView(APIView):
    permission_classes = []

    def get(self, request: Request) -> Response:
        search = request.query_params.get("search")
        q = Q()
        if search:
            q.add(Q(name__icontains=search), Q.AND)

        res = Course.objects.filter(q)

        serialized = CourseSerializer(res, many=True)
        return Response({"success": True, "data": {"courses": serialized.data}})

    def post(self, request: Request) -> Response:
        data = request.data
        q = Q()

        start_date = data.get("start_date")
        end_date = data.get("end_date")
        if start_date and end_date:
            q.add(Q(created_at__range=[start_date, end_date]), Q.AND)

        category = data.get("category")
        if category:
            q.add(Q(category__name__icontains=category), Q.AND)

        tutor_ids = data.get("tutors")
        if tutor_ids:
            courses_with_tutors = CourseTutor.objects.filter(
                tutor__id__in=tutor_ids
            ).values_list("course_id", flat=True)
            q.add(Q(id__in=courses_with_tutors), Q.AND)
        
        name = data.get("course")
        if name:
            q.add(Q(name__icontains=name), Q.AND)

        res = Course.objects.filter(q)
        serialized = CourseSerializer(res, many=True)
        return Response({"success": True, "data": {"courses": serialized.data}})


class CategoryListCreateView(APIView):
    permission_classes = [HasPermission]
    permission_dict = {"POST": ["add_category"]}

    def get(self, _request: Request) -> Response:
        categoryList = Category.objects.all()
        serialized = CategorySerializer(categoryList, many=True)
        response = {"success": True, "data": serialized.data}
        return Response(data=response, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serialized = CategorySerializer(data=request.data)
        if not serialized.is_valid():
            raise ValidationError(detail=serialized.errors)
        category: Category = serialized.save(created_by=request.user)
        response = {"success": True, "data": {"course_id": category.id}}
        return Response(data=response, status=status.HTTP_201_CREATED)


class CategoryManageView(APIView):
    permission_classes = [HasPermission]
    permission_dict = {"DELETE": ["delete_category"], "PATCH": ["update_category"]}

    def patch(self, request: Request, categoryid: UUID) -> Response:
        category = get_object_or_404(Category, id=categoryid)
        serialized = CategorySerializer(data=request.data)

        if not serialized.is_valid():
            raise ValidationError(detail=serialized.errors)

        if category.created_by != request.user:
            raise NotAuthenticated(detail="You are not the creator of this category.")

        category.name = request.data["name"]
        category.save()
        response = {"success": True, "data": []}
        return Response(data=response, status=status.HTTP_202_ACCEPTED)

    def delete(self, request: Request, categoryid: UUID):
        category = get_object_or_404(Category, id=categoryid)

        if category.created_by != request.user:
            raise NotAuthenticated(detail="You are not the creator of this category.")

        category.delete()
        response = {"success": True, "data": []}
        return Response(data=response, status=status.HTTP_202_ACCEPTED)


class ContentView(APIView):
    permission_classes = [IsAuthenticated]
    permission_dict = {}

    def get(self, request: Request, contentid: UUID):
        content = get_object_or_404(Content, id=contentid)
        if not Enrollment.objects.filter(course=content.chapter.course, learner=request.user).exists():
            raise ValidationError("User not enrolled in course")
        serialized = ContentSerializer(content)
        response = {"success": True, "data": serialized.data}
        return Response(data=response, status=status.HTTP_200_OK)

class LearnerEnrollView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, courseid: UUID):
        course = get_object_or_404(Course, id=courseid)
        enrollment = Enrollment.objects.create(learner=request.user, course=course)
        enrollment.save()
        return Response(data={"success": True, "data": []}, status=status.HTTP_202_ACCEPTED)

class ContentMarkCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, contentid: UUID):
        content = get_object_or_404(Content, id=contentid)
        ContentCompletionLog.objects.create(learner=request.user, content=content).save()
        return Response(data={"success": True, "data": []}, status=status.HTTP_202_ACCEPTED)
