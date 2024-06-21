# Create your views here.
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from .serializers import LoginSerializer
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status

from drf_spectacular.utils import extend_schema, OpenApiResponse


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
                "refresg_token": str(refresh_token),
            },
        }

        return Response(data=response, status=status.HTTP_200_OK)
