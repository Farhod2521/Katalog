from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView, ListAPIView, CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

import jwt, datetime

from .models import CatalogUsers, PasswordResets, ONEID
from .serializers import (
LoginSerializer, UserSerializer, UserTopAdsSerializer, 
PasswordResetRequestSerializer, PasswordResetConfirmSerializer,PasswordResetCodeSerializer, ONEIDSerializer, CatalogUsersSerializer

)
from django.utils.crypto import get_random_string

from app_company.models import Companies, AllAds
from app_materials.models import MaterialAds
from app_technos.models import TechnoAds
from app_machines_and_mechanisms.models import MMechanoAds
from app_small_mechanisms.models import SmallMechanoAds
from app_works.models import WorkAds
import uuid


from django.utils.timezone import now

from rest_framework.exceptions import AuthenticationFailed
SECRET_KEY = "dasjkdlajslkdjasd-asdalsjdlk23234l;kkas;dlkas"
class OneIDLoginView(APIView):
    def post(self, request):
        data = request.data
        pin = data.get("pin")
        user_id = data.get("user_id")
        birth_date = data.get("birth_date")
        passport_no = data.get("passport_no")
        birth_place = data.get("birth_place")
        full_name = data.get("full_name")

        if not pin or not user_id:
            return Response({"error": "PIN va user_id talab qilinadi"}, status=status.HTTP_400_BAD_REQUEST)

        # OneID foydalanuvchisini bazada borligini tekshiramiz yoki yaratamiz
        oneid_user, created = ONEID.objects.get_or_create(
            pin=pin,
            defaults={
                "user_id": user_id,
                "birth_date": birth_date,
                "passport_no": passport_no,
                "birth_place": birth_place,
                "full_name": full_name,
                "create_date": now()
            }
        )

        if not created:
            # Agar foydalanuvchi mavjud bo'lsa, ma'lumotlarini yangilaymiz
            oneid_user.user_id = user_id
            oneid_user.birth_date = birth_date
            oneid_user.passport_no = passport_no
            oneid_user.birth_place = birth_place
            oneid_user.full_name = full_name
            oneid_user.save()

        # Generate JWT token
        payload = {
            'id': oneid_user.id,
            'user_id': oneid_user.user_id,
            'role': "customer",
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return Response({
            "message": "Login muvaffaqiyatli",
            "token": token,
            "user": ONEIDSerializer(oneid_user).data
        }, status=status.HTTP_200_OK)

class LoginByDigitalSignatureView(APIView):
    serializer_class = None
    pagination_class = None
    def post(self, request):
#        print(request.data)
        if 'company_name' in request.data and 'company_stir' in request.data and request.data['company_name']!= 'НЕ УКАЗАНО'  and  request.data['company_name'] != "ЯККА ТАРТИБДАГИ ТАДБИРКОР":
            payload = {
            'company_stir': request.data['company_stir'],
            'company_name': request.data['company_name'],
            'company_ceo': request.data['company_ceo'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow(),
            "role":"company"
            }
            token = jwt.encode(payload, 'secret', 'HS256')
            response = Response()
            response.data = {
                "token": token,
                "role":"company",
            }
            company = Companies.objects.filter(company_stir=payload['company_stir']).first()
            if company is None:
                Companies.objects.create(
                    company_stir=request.data['company_stir'],
                    company_name=request.data['company_name'],
                    company_ceo=request.data['company_ceo']
                )

            return response
        else:
            raise AuthenticationFailed("No data")




import requests
from bs4 import BeautifulSoup

def orginfo(company_stir):
    company_name = None
    phone_number = None

    # First URL to fetch search results
    search_url = f"https://orginfo.uz/en/search/all/?q={company_stir}"
    response = requests.get(search_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the first relevant organization link
        card_titles = soup.find_all('h6', class_='card-title')
        for card in card_titles:
            company_name = card.text.strip()

        if company_name:
            org_link = None
            for link in soup.find_all('a', class_='text-decoration-none og-card', href=True):
                if '/organization/' in link['href']:
                    org_link = "https://orginfo.uz" + link['href']
                    break

            if org_link:
                org_response = requests.get(org_link)

                if org_response.status_code == 200:
                    org_soup = BeautifulSoup(org_response.text, 'html.parser')

                    phone_label = org_soup.find('label', {'for': 'smsCodeInput'})
                    if phone_label:
                        phone_number = phone_label.find('b').text.strip()

                return company_name, phone_number
        else:
            return None, None
    return None, None













class UserDSView(APIView):
    def get(self, request):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')

        response = Response()
        response.data = {
            "company_name": payload['company_name'],
            "company_stir": payload['company_stir'],
            "company_ceo": payload['company_ceo'],
            "role": "company",
            "menu": [
              {
                  "id": 1,
                  "title": "Bosh sahifa",
                  "url": "/dashboard",
              },
              {
                  "id": 2,
                  "title": "Materiallar va buyumlar",
                  "url": "/dashboard/materials",
              },
              {
                  "id": 3,
                  "title": "Mashina mexanizmlar",
                  "url": "/dashboard/machine-mechano",
              },
              {
                  "id": 4,
                  "title": "Qurilish ishlari",
                  "url": "/dashboard/works",
              },
              {
                  "id": 5,
                  "title": "Kichik mexanizatsiya",
                  "url": "/dashboard/small-mechano",
              },
              {
                  "id": 6,
                  "title": "Kompaniya haqida",
                  "url": "/dashboard/about",
              },
              {
                  "id": 7,
                  "title": "Buyurtmalar",
                  "url": "/dashboard/orders",
              },
            ]



        }
        return response




# Create your views here.
# class RegisterView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)



from captcha.models import CaptchaStore
from rest_captcha.serializers import RestCaptchaSerializer
from captcha.helpers import captcha_image_url

class LoginView(APIView):
    def get(self, request):
        # Generate a CAPTCHA key
        captcha_key = CaptchaStore.generate_key()
        
        # Construct the CAPTCHA image URL
        captcha_image_url = f"{request.scheme}://{request.get_host()}/captcha/image/{captcha_key}/"
        
        return Response({
            'captcha_image_url': captcha_image_url,
            'captcha_key': captcha_key
        })

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        captcha_key = serializer.validated_data['captcha_key']
        captcha_response = serializer.validated_data['captcha_response']

        # Verify CAPTCHA
        if not self.verify_captcha(captcha_key, captcha_response):
            return Response({'error': 'Invalid CAPTCHA'}, status=400)

        # Verify user credentials
        user = CatalogUsers.objects.filter(email=email, is_active=True).first()
        if user is None:
            raise AuthenticationFailed('User not found')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        # Generate JWT token
        payload = {
            'id': user.id,
            'stir': user.company,
            'role': "customer",
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, minutes=60),
            'iat': datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')

        return Response({
            'token': token,
            'id': user.id,
            'stir': user.company,
            'email': user.email,
            'role': "customer",
	    "menu" : [
        	{
           	 "id": 1,
           	 "title": "Mening buyurtmalarim",
           	 "url": "/dashboard/customer/my-orders",
        	},
		]
        })

    def verify_captcha(self, captcha_key, captcha_response):
        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
            return captcha.response == captcha_response
        except CaptchaStore.DoesNotExist:
            return False





from rest_framework.permissions import IsAuthenticated

class CatalogUsersListView(ListAPIView):
    serializer_class = CatalogUsersSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        email = self.request.query_params.get('email')
        if email:
            return CatalogUsers.objects.filter(email=email)
        return CatalogUsers.objects.none()  # Bo‘sh queryset qaytarish kerak

    def list(self, request, *args, **kwargs):
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Emailni kiriting !!!'}, status=400)

        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({'error': 'Bunday foydalanuvchi topilmadi!'}, status=404)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
 

class CatalogUsersUpdateView(UpdateAPIView):
    serializer_class = CatalogUsersSerializer     
    permission_classes = [IsAuthenticated]

    def get_object(self):
        email = self.request.data.get('email')
        return get_object_or_404(CatalogUsers, email=email)






# class Company_Profile_View(APIView):
#     permission_classes = [IsAuthenticated]  # Faqat autentifikatsiyalangan foydalanuvchilar kirishi mumkin

#     def get(self, request, *args, **kwargs):
#         company_stir = request.query_params.get('company_stir')

#         if not company_stir:
#             return Response({'error': 'company_stir ni kiriting!'}, status=400)

#         company = Companies.objects.filter(company_stir=company_stir).first()

#         if not company:F
#             return Response({'error': 'Bunday kompaniya topilmadi!'}, status=404)

#         serializer = CompaniesSerializer(company)
#         return Response(serializer.data, status=200)












class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('token')
        response.data = {
            'message': 'success'
        }
        return response
class UserView(APIView):
    def get(self, request):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')

        user = CatalogUsers.objects.filter(id=payload['id']).first()

        if user is None:
            return Response({"error": "User not found"}, status=404)

        serializer = UserSerializer(user)
        response_data = serializer.data
        response_data["menu"] = [
            {
                "id": 1,
                "title": "Mening buyurtmalarim",
                "url": "/dashboard/customer/my-orders",
            },
        ]

        return Response(response_data)

    def post(self, request):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')

        
        new_first_name = request.data['first_name']
        new_last_name = request.data['last_name']
        
        try:
            CatalogUsers.objects.filter(id=payload['id']).update(first_name=new_first_name, last_name=new_last_name)
            return Response(data="{'result': 'success'}")
        except Exception as e:
            return Response(data="{'result': 'error'}")


# class UserUpdateAPIView(UpdateAPIView):
#     def update(self, request):
#         token = request.META['HTTP_TOKEN']
#
#         if not token:
#             raise AuthenticationFailed('Invalid token, login again, please')
#
#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token expired, login again, please')
#
#
#         new_first_name = request.data['first_name']
#         new_last_name = request.data['last_name']
#
#         try:
#             CatalogUsers.objects.filter(id=payload['id']).update(first_name=new_first_name, last_name=new_last_name)
#             return Response(data="{'result': 'success'}")
#         except Exception as e:
#             return Response(data="{'result': 'error'}")
#
#


#
# class SetUserCompanyView(APIView):
#     def post(self, request):
#         token = request.META['HTTP_TOKEN']
#
#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token expired, login again, please')
#
#         user_id = payload['id']
#         stir = payload['company_stir']
#
#         company = Companies.objects.filter(company_stir=stir).first()
#
#         response = Response()
#
#         if company is None:
#             response.data = {
#                 "result": "error",
#                 "description": "Siz ro‘yhatdan o‘tgan STIR (Soliq to‘lovchining identifikatsion raqami) bo‘yicha ma'lumot topilmadi. STIRingizni tekshiring yoki Administratorga murojaat qiling!"
#             }
#             return response
#         elif company.company_owner is not None:
#             if company.company_owner_id == user_id:
#                 response.data = {
#                     "result": "succes",
#                     "description": "Sizga kompaniya biriktirilgan."
#                 }
#                 return response
#             else:
#                 response.data = {
#                     "result": "error",
#                     "description": "Siz ro‘yhatdan o‘tgan STIR (Soliq to‘lovchining identifikatsion raqami) boshqa foydalanuvchiga biriktirilgan. STIRingizni tekshiring yoki Administratorga murojaat qiling!"
#                 }
#                 return response
#         else:
#             try:
#                 Companies.objects.filter(company_stir=stir).update(company_owner=user_id)
#                 response.data = {
#                     "result": "success",
#                     "description": "Kompaniya muvaffaqiyatli biriktirildi"
#                 }
#                 return response
#             except Exception as e:
#                 response.data = {
#                     "result": "error",
#                     "description": e
#                 }
#                 return response


# Work with user statistics
class UserAdsStatView(APIView):
    serializer_class = None
    def get(self, request):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        response = Response()
        response.data = {
            'materials-ads': MaterialAds.objects.filter(company_stir=payload['company_stir']).count(),
            'machine-mechanos-ads': MMechanoAds.objects.filter(company_stir=payload['company_stir']).count(),
            'works-ads': WorkAds.objects.filter(company_stir=payload['company_stir']).count(),
            'small-mechanos-ads': SmallMechanoAds.objects.filter(company_stir=payload['company_stir']).count(),
            'technos-ads': TechnoAds.objects.filter(company_stir=payload['company_stir']).count()
        }
        return response



class UserTopAdsView(ListAPIView):
    pagination_class = None
    serializer_class = UserTopAdsSerializer
    def get_queryset(self):
        # token = request.META['HTTP_TOKEN']
        token = self.request.headers.get('TOKEN')

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        queryset = AllAds.objects.filter(company_stir=payload['company_stir']).values('material_name', 'material_type', 'material_url')[:7]
        # queryset = AllAds.objects.filter(company_stir='305826240')
        
        return queryset


#########################################################
##########################################################



from rest_framework.decorators import api_view
from rest_framework import status
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.http import HttpResponseBadRequest
import random
from django.shortcuts import get_object_or_404
import threading

class RegisterAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        verification_code = random.randint(1000, 9999)
        user = serializer.save()
        user.profile.verification_code = verification_code
        user.profile.save()

        # HTML dizaynli xabar
        email_subject = "ELEKTRON KLASSIFIKATOR - Tasdiqlash Kodingiz"
        email_body = f"""
        <div style="font-family: Arial, sans-serif; padding: 20px; text-align: center;">
            <h2 style="color: #333;">Tasdiqlash Kodingiz</h2>
            <p style="font-size: 18px; color: #555;">
                Hurmatli <strong>{user.first_name}</strong>, ro‘yxatdan o‘tganingiz uchun rahmat!<br>
                Sizning tasdiqlash kodingiz:
            </p>
            <div style="background-color: #f4f4f4; padding: 15px; display: inline-block; font-size: 22px; font-weight: bold; border-radius: 5px;">
                {verification_code}
            </div>
            <p style="color: #777; margin-top: 20px;">
                Agar bu xabar sizga noto‘g‘ri kelgan bo‘lsa, iltimos, uni e’tiborsiz qoldiring.
            </p>
        </div>
        """

        # Email jo‘natish funksiyasi
        def send_email():
            try:
                email = EmailMessage(
                    subject=email_subject,
                    body=email_body,
                    from_email="tmsiti.work@gmail.com",
                    to=[user.email],
                )
                email.content_subtype = "html"  # HTML formatda jo‘natish
                email.send()
            except BadHeaderError:
                return HttpResponseBadRequest("Invalid header found.")
            except Exception as e:
                return HttpResponse(f"Xatolik yuz berdi: {e}")


        email_thread = threading.Thread(target=send_email)
        email_thread.start()

        return Response({"detail": "Ro‘yxatdan o‘tish muvaffaqiyatli. Tasdiqlash kodi emailingizga yuborildi!"})
class VerifyEmailAPIView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        verification_code = request.data.get('verification_code')

        if not email or not verification_code:
            return Response({"detail": "Email and verification code are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CatalogUsers, email=email)
        if user.profile.verification_code == int(verification_code):
            user.profile.is_verified = True
            catalog_user = CatalogUsers.objects.get(email=email)
            catalog_user.is_active =True
            catalog_user.save()
            user.profile.save()
            return Response({"detail": "Email verified successfully."})
        else:
            return Response({"detail": "Invalid verification code."}, status=status.HTTP_400_BAD_REQUEST)



class ResendVerificationCodeAPIView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')

        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = get_object_or_404(CatalogUsers, email=email)
        verification_code = random.randint(1000, 9999)
        user.profile.verification_code = verification_code
        user.profile.save()

        try:
            send_mail(
                subject="ELEKTRON KLASSIFIKATOR",
                message=f"Sizning yangi tasdiqlash kodingiz: {verification_code}",
                from_email="abdikarimovfarhod2109@gmail.com", 
                recipient_list=[user.email],
            )
        except BadHeaderError:
            return HttpResponseBadRequest("Invalid header found.")
        except Exception as e:
            return HttpResponse(f"An error occurred: {e}")

        return Response({"detail": "Verification code resent successfully. Please check your email."})



@api_view(['POST'])
def password_change_view(request):
    try:
        old_password = request.data['old_password']
        new_password = request.data['new_password']
    except KeyError:
        return Response(
            data={'message': 'Old password or new password is missing'},
            status=status.HTTP_400_BAD_REQUEST
        )
    user = request.user
    if user.check_password(old_password):
        user.set_password(new_password)
        user.save()
        return Response(
            data={'message': 'Your password successfully changed!'},
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            data={'message': 'Old password entered wrong!'},
            status=status.HTTP_400_BAD_REQUEST
        )
    





class PasswordResetRequestAPIView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = CatalogUsers.objects.filter(email=email).first()
        if user:
            reset_code = get_random_string(length=5)
            PasswordResets.objects.create(user=user, reset_code=reset_code)
            try:
                send_mail(
                    subject="Elektron Klassifikator Parol tiklash",
                    message=f'Sizning kodingiz  --- {reset_code}',
                    from_email="abdikarimovfarhod2109@gmail.com",
                    recipient_list=[user.email],
                )
            except BadHeaderError:
                return Response({"detail": "Invalid header found."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"detail": f"An error occurred: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"detail": "Password reset email has been sent."}, status=status.HTTP_200_OK)

from django.utils import timezone
class PasswordResetCodeAPIView(GenericAPIView):
    serializer_class = PasswordResetCodeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_code = serializer.validated_data['reset_code']
        reset_record = PasswordResets.objects.filter(reset_code=reset_code, status=True, created_at__gte=timezone.now()-timezone.timedelta(hours=1)).first()
        if reset_record:
            return Response({"detail": "Reset code is valid.", "reset_code": reset_code}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid or expired reset code."}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        reset_code = request.data.get('reset_code')
        if not reset_code:
            return Response({"detail": "Reset code is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        reset_record = PasswordResets.objects.filter(reset_code=reset_code, status=True, created_at__gte=timezone.now()-timezone.timedelta(hours=1)).first()
        if not reset_record:
            return Response({"detail": "Invalid or expired reset code."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data['new_password']

        user = reset_record.user
        user.set_password(new_password)
        user.save()
        reset_record.status = False
        reset_record.save()
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)

