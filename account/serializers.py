from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from account.models import Otp, Forgot
from .signals import get_otp
from django.core.mail import send_mail

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255, write_only=True)
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['id','first_name', 'last_name', 'email', 'password','phone', 'date_joined']



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=255)

    
class ForgotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forgot
        fields = ['email_forgot']  


class ResetSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)
    re_password = serializers.CharField(max_length=255)


class VerifyOTPSerializer(serializers.Serializer):
    otp=serializers.CharField(max_length=6)
    
    
    def verify(self):
        otp = self.validated_data['otp']
        try:
            otp = Otp.objects.get(code=otp)
        except Otp.DoesNotExist:
            raise ValidationError(detail={
                "error":"Invalid OTP"
            })
        except Exception:
            Otp.objects.filter(code=otp).delete()
            raise ValidationError(detail={
                "error":"Unable to fetch OTP"
            })
            
        
        if otp.is_expired():
            raise ValidationError(detail={
                "error":"OTP Expired"
            })
        else:
            if otp.user.is_active != True:
                otp.user.is_active=True
                otp.user.save()
                return otp.user
            else:
                raise ValidationError(detail={
                "error":"User with this OTP already active"
            })
                
class VerifyPasswordOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    password = serializers.CharField(max_length=255)
    re_password = serializers.CharField(max_length=255)

    def verify(self):
        otp = self.validated_data['otp']
        try:
            otp = Otp.objects.get(code=otp)
        except Otp.DoesNotExist:
            raise ValidationError(detail={
                "error":"Invalid OTP"
            })    
        except Exception:
            Otp.objects.filter(code=otp).delete()
            raise ValidationError(detail={
                "error":"unable to fetch OTP"
            })

        if otp.is_expired():
            raise ValidationError(detail={
                "error": "OTP expired"
            })    
        else:          
                return otp.user               
                
class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    
    def get_new_otp(self):
        email = self.validated_data['email']
        
        if User.objects.filter(email=email, is_active=False).exists():
            user = User.objects.get(email=email)
            otp, expiry_date = get_otp(6)
            
            Otp.objects.create(code=otp, user=user, expiry_date=expiry_date)
            message= f"""Welcome {user.first_name}!
Your activation OTP is {otp}.
Expires in 2 minutes. 
Regards,
Learn-Ed"""

            send_mail(
                subject="NEW OTP VERIFICATION CODE",
                message=message,
                from_email='Klinsman from SenseiKido',
                recipient_list=[user.email]
            )
            
            return {"message":"please check your email for new otp"}
        else:
            raise ValidationError(detail={
                    "error":"Unable to get a user with this email"
                })


