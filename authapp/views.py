import datetime
from ftplib import FTP
import random
import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.utils import timezone
# from django.contrib.auth.models import User
import re
from django.contrib.auth import get_user_model
from authapp.methods.helper import is_email, is_phone, send_email_async, generate_otp
from .models import CustomUser,OTP
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from methodism import METHODISM
from authapp import methods
class Main(METHODISM):
    file = methods
    token_key = 'Token'
    not_auth_methods=[]
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
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
        token = Token.objects.create(user=user)

        return Response({
            'message': "Ro'yxatdan o'tish ma'lumotlari to'g'ri.",
            'Token': token.key
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

User = get_user_model()

class Authone(APIView):
    def post(self, request):
        data = request.data
        contact = data.get('contact')  

        if not contact:
            return Response({"error": "Telefon raqami yoki email kiritilmadi"}, status=400)

        if is_email(contact):
            if User.objects.filter(email=contact).exists():
                raise ValidationError("Bu email allaqachon ro'yxatdan o'tgan.")

            key = f"{uuid.uuid4()}"
            send_email_async(contact)
            return Response({
                "message": "Tasdiqlash email yuborildi",
                "token": key
            })

        elif is_phone(contact):
            if User.objects.filter(phone=contact).exists():
                raise ValidationError("Bu raqam allaqachon ro'yxatdan o'tgan.")

            code, key = generate_otp(contact)
            print(f"Kod: {code}") 

            return Response({
                "otp": code,
                "token": key
            })

        else:
            return Response({"error": "Noto‘g‘ri formatdagi telefon yoki email"}, status=400)

class AuthTwo(APIView):
    def post(self, request):
        data = request.data
        if not data.get('code') or not data.get('key'):
            return Response({ "error": "Siz to‘liq ma’lumot kiritmadingiz" })

        otp = OTP.objects.filter(key=data['key']).first()
        if not otp:
            return Response({ "error": "Noto‘g‘ri key" })

        now = timezone.now()
        if (now - otp.created).total_seconds() >= 180:
            otp.is_expire = True
            otp.save()
            return Response({ "error": "Key yaroqsiz (vaqti o‘tdi)" })

        if otp.is_conf:
            return Response({ "error": "Ushbu kod allaqachon ishlatilgan" })

        if data['code'] != otp.key[-4:]:
            otp.tried += 1
            otp.save()
            return Response({ "error": "Siz xato kod kiritdingiz" })

        otp.is_confirmed = True
        otp.save()

        user = CustomUser.objects.filter(phone=otp.phone).first()
        return Response({ "registered": True })