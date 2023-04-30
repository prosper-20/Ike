from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from .models import Otp
from django.contrib.auth import get_user_model
import random
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings



