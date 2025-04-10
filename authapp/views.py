from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.contrib.auth.models import User
import re
from .models import CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        phone = data.get('phone')
        password = data.get('password')

        if len(phone) > 9:
            raise ValidationError("Telefon raqami 9 raqamdan ko'p bo'lmasligi kerak.")
        
        if User.objects.filter(profile__phone=phone).exists(): 
            raise ValidationError("Ushbu telefon raqami allaqachon ro'yxatdan o'tgan.")

        if len(password) < 6:
            raise ValidationError("Parol kamida 6 ta belgidan iborat bo'lishi kerak.")
        
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Parol kamida bitta katta harfni o'z ichiga olishi kerak.")
        user_data = {
            'phone': phone,
            'password': password,
        }
        user = CustomUser.objects.filter(phone=data[phone]).first()
        token = Token.objects.create(user=user)
        if not authenticate(request, phone=data['phone'],password=data['password']):
            return Response({
                "Error":"error"
            })
            
            
        return Response({
            'message': 'Ro\'yxatdan o\'tish ma\'lumotlari to\'g\'ri.',
            "Token":token
        })
class LogOutView(APIView):
    permission_classes=IsAuthenticated
    authentication_classes = TokenAuthentication
    def post(self,request):
        token = Token.objects.filter(user=request.user).first()
        token.delete()
        return Response({
            "Message":"Siz tizimdan chiqdingiz"
        })
class LogInView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "message": "Tizimga muvaffaqiyatli kirdingiz"
            })
        else:
            return Response({
                "error": "Login yoki parol noto‘g‘ri"
            }, status=401) 
class Profile(APIView):
    permission_classes=IsAuthenticated
    authentication_classes=TokenAuthentication
    
    def get(self,request):
        user = request.user
        return user.format
    def put(self, request):
        user = request.user
        data = request.data

        new_phone = data.get('phone', user.phone)

        if new_phone != user.phone:
            if CustomUser.objects.filter(phone=new_phone).exists():
                return Response({
                    'Error': 'Bu telefon raqami bilan boshqa foydalanuvchi mavjud'
                }, status=400)

        user.name = data.get('name', user.name)
        user.phone = new_phone
        user.save()

        return Response({
            "Message": True
        })
    def delete(self, request):
        user = request.user
        user.delete()
        return Response({
            "message": "Foydalanuvchi muvaffaqiyatli o'chirildi"
        }, status=204)
        
