# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import LoginSerializer, TutorSignupSerializer, LearnerSignupSerializer, TutorListSerializer
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework import status
from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema, OpenApiResponse

from iam.models import AppUser

USER = get_user_model()

class LoginView(APIView):
    permission_classes = []
    serializer_class = LoginSerializer

    @extend_schema(
        summary="Login as a user",
        responses={
            201: OpenApiResponse(description="Access Token and Refresh Token"),
            400: OpenApiResponse(description="Bad request (something invalid)"),
        },
    )
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        user = authenticate(request=request, **serializer.validated_data)
        if user is None:
            raise ValidationError(detail="Invalid username or password")

        refresh_token: RefreshToken = RefreshToken().for_user(user)
        access_token: AccessToken = refresh_token.access_token

        update_last_login(None, user)

        response = {
            "success": True,
            "data": {
                "access_token": str(access_token),
                "refresh_token": str(refresh_token),
            },
        }

        return Response(data=response, status=status.HTTP_200_OK)

class CustomTokenRefreshView(TokenRefreshView):
    permission_classes = []
    serializer_class = TokenRefreshSerializer

class LearnerSignupView(APIView):
    permission_classes = []
    serializer_class = LearnerSignupSerializer

    def post(self, request: Request) -> Response:
        serializer = LearnerSignupSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        user: AppUser = serializer.save()

        response_data = {
            "success": True,
            "data": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            },
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)


class TutorSignupView(APIView):
    permission_classes = []
    serializer_class = TutorSignupSerializer

    def post(self, request: Request) -> Response:
        serializer = TutorSignupSerializer(data=request.data)
        if not serializer.is_valid():
            raise ValidationError(detail=serializer.errors)

        user: AppUser = serializer.save()

        response_data = {
            "success": True,
            "data": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            },
        }
        return Response(data=response_data, status=status.HTTP_201_CREATED)
    
class TutorsListView(APIView):
    permission_classes = []

    def get(self, request: Request) -> Response:
        tutors = USER.objects.filter(role = "TUTOR")
        serialized = TutorListSerializer(tutors, many=True)
        response_data = {
            "success": True,
            "data": serialized.data
        }
        return Response(data=response_data, status=status.HTTP_200_OK)