from django.db import models

from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # добавьте любые дополнительные поля здесь
    pass
