from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserSerializer


class RegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Debugging print statements
        print(f"Attempting to authenticate user: {username}")

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)

            # Debugging print statements
            print("User authenticated successfully")

            return Response({
                'userid': user.id,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            # Debugging print statements
            print("Authentication failed")

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
