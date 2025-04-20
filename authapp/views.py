import datetime
from ftplib import FTP
import random
import uuid
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


class Authone(APIView):
    
    def post(self,request):
        data = request.data
        phone = data.get('phone')
        if data['phone']:
            return Response({
                "error":"Togri malumot kiritilmagan"
            }) 
            
        if len(phone) > 9 or not isinstance(phone,int):
            raise ValidationError("Telefon raqami notogri kiritilgan.")
        
        if User.objects.filter(profile__phone=phone).exists(): 
            raise ValidationError("Ushbu telefon raqami allaqachon ro'yxatdan o'tgan.")
        code = ''.join([str(random.randint(1,999999))[-1] for _ in range(6)])
        key= uuid.uuid4().__str__()+code
        otp = OTP.objects.create(phone=phone,key=key)
        # int_= string.digits
        # str_=string.ascii_letters
        return Response({
            "otp":code,
            'token':key
        })
class AuthTwo(APIView):
    def post(self,reques):
        data = reques.data
        if not data['code'] or not data['key']:
            return Response({
                "error":"Siz toliq malumot kiritmadingiz"
            })
        otp = OTP.objects.filter(key=data['key']).first()
        
        if not otp:
            return Response({
                "Error":"xato key" 
            })
        now = datetime.datetime(datetime.timezone.utc)
        if (now-otp.created).total_seconds()>=180:
            otp.is_expire =True
            otp.save()
            return Response({
                "error":"key yaroqsiz"
            })
            
        if otp.is_conf:
            return Response({
                "Error":"Eskirgan key"
            })
        
        if data['code'] != data ['key'][-4]:
            otp.tried+=1
            otp.save()
            return Response({
                "Error":"Siz xato kod kiritdingiz"
            })
        
        otp.is_conf=True
        otp.save()
        user = CustomUser.objects.filter(phone=otp.phone).first()
        
        
        return Response({
            "Registered":True is not None
        })
        