from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.conf import settings
import requests
@api_view(['POST'])
def verify_captcha(request):
    captcha_value = request.data.get('captchaValue')
    secret_key = settings.RECAPTCHA_SECRET_KEY
    captcha_verification_url = 'https://www.google.com/recaptcha/api/siteverify'

    response = requests.post(
        captcha_verification_url,
        data={'secret': secret_key, 'response': captcha_value}
    )
    result = response.json()

    if result.get('success'):
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error-codes': result.get('error-codes')})
