from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
# from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserSerializer


# @method_decorator(ratelimit(key="ip", rate="5/m", method="POST"), name="post")
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user",
        request_body=UserRegistrationSerializer,
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(ratelimit(key="ip", rate="10/m", method="POST"), name="post")
class LoginView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Login user",
        request_body=UserLoginSerializer,
        tags=["Authentication"],
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
