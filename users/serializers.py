from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from app_company.models import Companies, AllAds
from rest_framework import serializers
from .models import CatalogUsers, ONEID
from captcha.models import CaptchaStore


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    captcha_key = serializers.CharField()
    captcha_response = serializers.CharField()

    def validate(self, data):
        # Validate CAPTCHA
        captcha_key = data.get('captcha_key')
        captcha_response = data.get('captcha_response')
        if not self.validate_captcha(captcha_key, captcha_response):
            raise serializers.ValidationError({'captcha': 'Invalid CAPTCHA'})
        return data

    def validate_captcha(self, captcha_key, captcha_response):
        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key)
            return captcha.response == captcha_response
        except CaptchaStore.DoesNotExist:
            return False



class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'password', 'company']
        extra_kwargs = {
            'password': {'write_only': True}
        }


    def validate(self, data):
        errors = {}

        # Telefon raqam tekshirish
        User = get_user_model()
        if User.objects.filter(phone=data.get('phone')).exists():
            errors['phone'] = "Bu telefon raqami allaqachon mavjud."

        # Email tekshirish
        if User.objects.filter(email=data.get('email')).exists():
            errors['email'] = "Bu email allaqachon mavjud."

        # company tekshirish (agar modelda bo‘lsa)
        if 'company' in data and User.objects.filter(inn=data.get('company')).exists():
            errors['company'] = "Bu pnfl allaqachon mavjud."

        if errors:
            raise serializers.ValidationError(errors)

        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.is_active = False
        instance.save()
        return instance
    
   

    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.save()
        return instance





# class UsersSerializer(ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = ['id', 'username', 'first_name', 'last_name', 'email']
#         # fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']


class UserTopAdsSerializer(ModelSerializer):
    # material_code = SerializerMethodField()
    class Meta:
        model = AllAds
        fields = ['material_name', 'material_type', 'material_url']

class ONEIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = ONEID
        fields = '__all__'


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
class PasswordResetCodeSerializer(serializers.Serializer):
    reset_code = serializers.CharField(max_length=10)

class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128)
