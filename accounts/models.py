from django.db import models
import os
import binascii
from django.contrib.auth.models import User
from django.core.mail import send_mail
from shop_api.settings import EMAIL_HOST_USER



# Create your models here.

class ConfirmUser(models.Model):
    code = models.CharField(default=binascii.hexlify(os.urandom(4)).decode(), blank=True,max_length=16)
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_confirm')
    created = models.DateTimeField(auto_now_add=True)

    def send_email(self):
        send_mail('КОД ПОДТВЕРЖДЕНИЯ',
                  self.code,
                  EMAIL_HOST_USER,
                  [self.user.email],
                  fail_silently=False)
