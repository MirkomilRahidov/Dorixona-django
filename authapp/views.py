from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
import re

User = get_user_model()

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        phone = data.get('phone')
        password = data.get('password')

        if not phone or not password:
            raise ValidationError("Telefon va parol majburiy.")

        if len(password) < 6:
            raise ValidationError("Parol kamida 6 ta belgidan iborat bo'lishi kerak.")
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Parol kamida bitta katta harf bo'lishi kerak.")

        if CustomUser.objects.filter(phone=phone).exists():
            raise ValidationError("Bu raqam allaqachon ro'yxatdan o'tgan.")

        user = CustomUser.objects.create_user(phone=phone, password=password)
        tokens = get_tokens_for_user(user)

        return Response({
            'message': "Ro'yxatdan o'tish muvaffaqiyatli.",
            'tokens': tokens
        })

class LoginView(APIView):
    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        user = authenticate(phone=phone, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({
                "message": "Tizimga muvaffaqiyatli kirdingiz.",
                "tokens": tokens
            })
        else:
            return Response({
                "error": "Login yoki parol noto‘g‘ri"
            }, status=401)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Tizimdan chiqdingiz"})
        except Exception as e:
            return Response({"error": "Token noto‘g‘ri yoki allaqachon yaroqsiz"}, status=400)
