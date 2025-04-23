# authapp/methods/auth.py

import datetime
import random
import uuid

from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from methodism import custom_response, MESSAGE
from authapp.models import CustomUser, OTP


def register(request, params):
    phone = params.get('phone')
    password = params.get('password')

    if not phone or not password:
        return custom_response(status=False, message=MESSAGE['DataNotFull'])

    if len(password) < 6 or not any(c.isupper() for c in password):
        return custom_response(status=False, message=MESSAGE['PasswordError'])

    if CustomUser.objects.filter(phone=phone).exists():
        return custom_response(status=False, message=MESSAGE['UserAlreadyDeleted'])

    user = CustomUser.objects.create_user(phone=phone, password=password)
    token = Token.objects.create(user=user)

    return custom_response(
        status=True,
        data={'token': token.key},
        message=None
    )


def login(request, params):
    user = CustomUser.objects.filter(phone=params.get('phone')).first()
    if not user:
        return custom_response(status=False, message=MESSAGE['Unauthenticated'])

    if not user.check_password(params.get('password', '')):
        return custom_response(status=False, message=MESSAGE['PasswordError'])

    token, _ = Token.objects.get_or_create(user=user)
    return custom_response(
        status=True,
        data={'token': token.key},
        message=None
    )


def logout(request, params):
    user = request.user
    Token.objects.filter(user=user).delete()
    return custom_response(status=True, message=MESSAGE['LogedOut'])


def auth_one(request, params):
    phone = params.get('phone')
    if not phone:
        return custom_response(status=False, message=MESSAGE['DataNotFull'])

    if not isinstance(phone, (str, int)) or len(str(phone)) != 9:
        return custom_response(status=False, message=MESSAGE['InvalidBasicHeader1'])

    if CustomUser.objects.filter(phone=phone).exists():
        return custom_response(status=False, message=MESSAGE['UserAlreadyDeleted'])

    code = ''.join(str(random.randint(0, 9)) for _ in range(6))
    key = f"{uuid.uuid4()}{code}"

    OTP.objects.create(phone=phone, key=key)

    return custom_response(
        status=True,
        data={'otp': code, 'token': key},
        message=None
    )


def auth_two(request, params):
    code = params.get('code')
    key = params.get('key')

    if not code or not key:
        return custom_response(status=False, message=MESSAGE['DataNotFull'])

    otp = OTP.objects.filter(key=key).first()
    if not otp:
        return custom_response(status=False, message=MESSAGE['NotData'])

    now = datetime.datetime.now(datetime.timezone.utc)
    if (now - otp.created).total_seconds() >= 180:
        otp.is_expire = True
        otp.save()
        return custom_response(status=False, message=MESSAGE['TokenUnUsable'])

    if otp.is_conf:
        return custom_response(status=False, message=MESSAGE['TokenUnUsable'])

    if code != key[-6:]:
        otp.tried += 1
        otp.save()
        return custom_response(status=False, message=MESSAGE['PasswordError'])

    otp.is_conf = True
    otp.save()

    return custom_response(status=True, data={'verified': True}, message=None)
