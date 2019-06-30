from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_auth.views import LoginView
from rest_auth.registration.views import RegisterView
from .serializers import CustomRegisterSerializer, CustomUserDetailsSerializer

User = get_user_model()


class CustomLoginView(LoginView):
    pass

class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer

class CustomUserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    serializer_class = CustomUserDetailsSerializer

    def get_object(self):
        return self.request.user
