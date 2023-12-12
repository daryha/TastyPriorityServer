from django.shortcuts import render

from django.http import JsonResponse
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt 
import json

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        try:
            send_mail(
                'Поздравляем с подарком!',
                'Ура, вы успешно получили coca-cola в подарок. Желаем вам счастливого нового года! @TastyPriority',
                'daryha56@gmail.com', 
                [email],
                fail_silently=False,
            )
            return JsonResponse({'success': 'Письмо отправлено успешно!'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)
