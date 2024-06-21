# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status

from .models import Course
from .serializers import CourseListSerializer
from AcadMe.permissions import HasPermission


class CourseView(APIView):
    permission_classes = [HasPermission]
    permission_dict = {"POST": ["add_course"]}

    def get(self, _request: Request) -> Response:
        courseList = Course.objects.all()
        serialized = CourseListSerializer(courseList, many=True)
        response = {"success": True, "data": serialized.data}
        return Response(data=response, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        pass
