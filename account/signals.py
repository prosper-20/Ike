from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from .models import Otp, Forgot
from django.contrib.auth import get_user_model
import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token

User = get_user_model()

def get_otp(n):
    code = "".join([str(random.choice(range(0,10))) for _ in range(n)])
    expiry_date = timezone.now() + timezone.timedelta(minutes=2)
    return code, expiry_date


@receiver(post_save, sender=User)
def send_otp(sender, instance, created, *args, **kwargs):
    
    if created and instance.is_superuser != True:
        
        code, expiry_date = get_otp(6)
        
        Otp.objects.create(code=code, user=instance, expiry_date=expiry_date)
        
        message= f"""Welcome {instance.first_name}!
# You have successfully registered on our platform and ready to begin learning with us! 
# Your activation OTP is {code}.
# Expires in 2 minutes 
# Regards,
# Learn-Ed"""

        send_mail(
            subject="OTP VERIFICATION CODE",
            message=message,
            from_email="ikechukwuklinsman@gmail.com",
            recipient_list=[instance.email]
        )

@receiver(post_save, sender=Forgot)
def send_otp_forgot(sender, instance, created, *args, **kwargs):
    forgetter = User.objects.get(email=instance.email_forgot)
         
    code, expiry_date = get_otp(6)
    
    Otp.objects.create(code=code, user=forgetter, expiry_date=expiry_date)
    
    message= f"""Welcome {forgetter.first_name}!
You have successfully reset your password. Your activation OTP is {code}.
Expires in 2 minutes 
Regards,
Learn-Ed"""

    send_mail(
        subject="OTP VERIFICATION CODE",
        message=message,
        from_email="ikechukwuklinsman@gmail.com",
        recipient_list=[forgetter.email]
    )

@receiver(post_save, sender=User)
def payment_made(sender, instance, created, **kwargs):
    if instance.is_payment == True:
        
        message= f"""Hello {instance.first_name}!
# You now have access to the courses! 
# Click on the link to view your courses.
# Regards,
# Learn-Ed""" 

        send_mail(
            subject="COURSE LINK",
            message=message,
            from_email="ikechukwuklinsman@gmail.com",
            recipient_list=[instance.email]
        )
# @receiver(pre_save, sender=User)
# def create_auth_token(sender, instance, created= False, **kwargs):
#     if instance.is_active:
#         token = Token.objects.create(user=instance)

#         message= f"""Hello {instance.first_name}!
# # You have successfully activated your account! 
# # Your Token number is {token}.
# # Regards,
# # Learn-Ed""" 

#         send_mail(
#             subject="OTP VERIFICATION CODE",
#             message=message,
#             from_email="ikechukwuklinsman@gmail.com",
#             recipient_list=[instance.email]
#         )