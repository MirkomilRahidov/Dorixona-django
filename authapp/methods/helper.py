import re
import threading
import random
import uuid
from authapp.models import OTP

def is_email(value):
    return re.match(r"[^@]+@[^@]+\.[^@]+", value)

def is_phone(value):
    return re.match(r"^\+?\d{9,15}$", value)

def send_email(email):
    print(f"Emailga tasdiqlash xati yuborildi: {email}")

def send_email_async(email):
    threading.Thread(target=send_email, args=(email,)).start()

def generate_otp(phone):
    code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    key = f"{uuid.uuid4()}-{code}"
    OTP.objects.create(phone=phone, key=key)
    return code, key
    
