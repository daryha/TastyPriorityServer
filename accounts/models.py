from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
from django.utils import timezone




class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        super(CustomUser, self).save(*args, **kwargs)


CustomUserModel = get_user_model()


class PasswordResetToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reset_tokens')
    code = models.CharField(max_length=6)  # Изменено на фиксированную длину 6
    created_at = models.DateTimeField(auto_now_add=True)

    def is_token_valid(self):
        """Check if the code is still valid within 24 hours."""
        return (timezone.now() - self.created_at) < timezone.timedelta(hours=24)

    def __str__(self):
        """String representation of the PasswordResetToken."""
        return f"Password reset code for {self.user}"

    @staticmethod
    def generate_reset_code():
        """Generate a random string of 6 digits."""
        return get_random_string(6, allowed_chars='0123456789')