from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
# Create your models here.

USER_ROLE  = (
    ('admin', 'admin'),
    ("company", 'company'),
    ('manager', 'manager'),
    ('customer', 'customer'),
)



class ONEID(models.Model):
    pin =  models.IntegerField(unique=True)
    user_id =  models.CharField(max_length=50, null=True, blank=True)
    birth_date =  models.CharField(max_length=20)
    passport_no = models.CharField(max_length=15)
    birth_place =  models.CharField(max_length=255)
    full_name  =  models.CharField(max_length=277)
    create_date =  models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "oneID"




class CatalogUsers(AbstractUser):
    email = models.EmailField(verbose_name='Elektron pochta', unique=True)
    password = models.CharField(max_length=255)
    company = models.CharField(verbose_name='Kompaniya ID', unique=True, max_length=9)
    role =  models.CharField(max_length=10, choices=USER_ROLE, default="customer")
    phone = models.CharField(verbose_name='Asosiy telefon raqami', max_length=15, help_text='Iltimos, +99871-1234567 yoki +99890-1234567 shaklida to‘ldiring', null=True, blank=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['company']

    class Meta:
        db_table = 'catalog_users'



class PasswordResets(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reset_code = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        db_table = 'app_passwordreset'






class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    verification_code = models.IntegerField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = 'app_profile_verify'






