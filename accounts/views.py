from django.contrib.auth import get_user_model, authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated  # Добавленный импорт
from .serializers import UserSerializer
from .models import PasswordResetToken, CustomUser
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import logging



User = get_user_model()



@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Неправильный логин или пароль"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
        profile_data = {
            'username': request.user.username,
            'email': request.user.email,
            # Другие поля профиля
        }
        return Response(profile_data, status=status.HTTP_200_OK)




# Дополнительные импорты и настройки остаются без изменений


@api_view(['POST'])
def password_reset_request(request):
    email = request.data.get('email').lower()
    user = CustomUser.objects.filter(email=email).first()

    if user:
        # Генерация случайного кода
        code = get_random_string(6, allowed_chars='0123456789')
        # Сохранение кода в базу данных
        reset_code, created = PasswordResetToken.objects.update_or_create(
            user=user, defaults={'code': code})

        # Текст сообщения (не меняется)
        message = (f"Здравствуйте, {email}\n\n"
                   "Мы получили запрос на отправку разового кода для вашей учетной записи TastyPriority.\n\n"
                   f"Ваш разовый код: {code}\n\n"
                   "Если вы не запрашивали этот код, можете смело игнорировать это сообщение электронной почты. "
                   "Возможно, кто-то ввел ваш адрес электронной почты по ошибке.\n\n"
                   "С уважением,\n"
                   "Служба технической поддержки учетных записей TastyPriority")

        send_mail('Ваш код для сброса пароля', message, 'support@tastypriority.com', [email], fail_silently=False)

    return Response({"message": "Если учетная запись с таким email найдена, сообщение для сброса пароля было отправлено."}, status=status.HTTP_200_OK)

logger = logging.getLogger(__name__)

@api_view(['POST'])
def reset_password_confirm(request):
        email = request.data.get('email')
        code = request.data.get('code')
        new_password = request.data.get('newPassword')

        if not all([email, code, new_password]):
            return Response({'error': 'Missing parameters'}, status=status.HTTP_400_BAD_REQUEST)

        logger.info(f"Received data: {request.data}")

        try:
            user = User.objects.get(email=email)
            reset_token = PasswordResetToken.objects.get(user=user, code=code)
        except (User.DoesNotExist, PasswordResetToken.DoesNotExist):
            return Response({'error': 'Invalid email or code'}, status=status.HTTP_400_BAD_REQUEST)

        if reset_token.is_token_valid():
            user.set_password(new_password)
            user.save()
            reset_token.delete()  # Удалить использованный код сброса
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'code expired or invalid'}, status=status.HTTP_400_BAD_REQUEST)