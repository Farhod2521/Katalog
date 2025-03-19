from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Regions(models.Model):
    region_name = models.CharField(max_length=1, null=True, blank=True)
    region_name_uz = models.CharField(verbose_name='Viloyat(shahar) nomi', max_length=30)
    region_name_en = models.CharField(verbose_name='Region/city', max_length=30, null=True, blank=True)
    region_name_ru = models.CharField(verbose_name='Вилоят/город', max_length=30, null=True, blank=True)

    def __str__(self):
        return self.region_name_uz

    class Meta:
        db_table = 'uzb_regions'


class Districts(models.Model):
    district_name = models.CharField(max_length=1, null=True, blank=True)
    district_name_uz = models.CharField(verbose_name='Tuman(shahar, posyolka, ovul) nomi', max_length=25)
    district_name_en = models.CharField(verbose_name='Район/город', max_length=25, null=True, blank=True)
    district_name_ru = models.CharField(verbose_name='District/city', max_length=25, null=True, blank=True)
    district_region = models.ForeignKey(Regions, verbose_name='Viloyat', on_delete=models.PROTECT)
    district_type = models.BooleanField(verbose_name='Toifasi: (shahar/tuman)', default=1)

    def __str__(self):
        return self.district_name_uz

    class Meta:
        db_table = 'uzb_districts'


class Companies(models.Model):
    company_stir = models.CharField(verbose_name='Soliq to‘lovchining identifikatsion raqami (STIR, ИНН)', max_length=9, primary_key=True)
    company_name = models.CharField(verbose_name='Tashkilot(kompaniya, korxona, muassasa, firma, ...) nomi', max_length=500)
    company_reg_year = models.DateField(verbose_name='Ro‘yhatga olingan sana', null=True, blank=True)
    company_region = models.ForeignKey(Regions, verbose_name='Viloyat', null=True, blank=True, on_delete=models.DO_NOTHING)
    company_district = models.ForeignKey(Districts, verbose_name='Tuman', null=True, blank=True, on_delete=models.DO_NOTHING)
    company_address = models.CharField(verbose_name='Manzil', max_length=255, null=True, blank=True)
    company_latitude = models.FloatField(null=True, blank=True)
    company_longitude = models.FloatField(null=True, blank=True)
    company_email = models.EmailField(verbose_name='Elektron pochta', max_length=50, null=True, blank=True)
    company_phone_main = models.CharField(verbose_name='Asosiy telefon raqami', max_length=15, help_text='Iltimos, +99871-1234567 yoki +99890-1234567 shaklida to‘ldiring', null=True, blank=True)
    company_logo = models.ImageField(verbose_name='Logotip', upload_to='companies/', null=True, blank=True)
    statuses = {
        (1, 'Aktiv'),
        (0, 'Nofaol'),
    }
    company_status = models.CharField(verbose_name='Holati', max_length=1, choices=statuses, default=1)
    company_ceo = models.CharField(verbose_name='Rahbar FIO', max_length=50, null=True, blank=True)
    company_phone_other = models.CharField(verbose_name='Qo‘shimcha telefon raqamlari', max_length=50, help_text='Iltimos, +99871-1234567, +99890-1234567 shaklida to‘ldiring', null=True, blank=True)
    company_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)
    company_owner = models.OneToOneField(get_user_model(), verbose_name='Kompaniya egasi', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.company_name + ', [STIR: ' + self.company_stir + ']'

    class Meta:
        db_table = 'companies'


class AllAds(models.Model):
    material_image = models.ImageField(verbose_name='Material uchun rasm', upload_to='media/ads/materials/', null=True, blank=True)
    material_type = models.CharField(max_length=50)
    material_name = models.CharField(max_length=25)
    material_url = models.CharField(max_length=50)
    material_description = models.TextField(verbose_name='Material tavsifi', max_length=500, blank=True, null=True)
    sertificate_blank_num = models.CharField(verbose_name='Maxsulot sertifikat blanka raqami', max_length=10)
    sertificate_reestr_num = models.CharField(verbose_name='Maxsulot sertifikat reestr raqami', max_length=10)
    material_price = models.FloatField(verbose_name='Material narxi')
    material_price_currency = models.CharField(verbose_name='Narx ko‘rsatilgan valyuta', default='UZS', max_length=15)
    material_measure = models.CharField(verbose_name='Material o‘lchov birligi', max_length=25, default='kg')
    material_amount = models.FloatField(verbose_name='Material miqdori (Ishlab chiqarish/yetkazib berish qobiliyati)')
    material_amount_measure = models.CharField(verbose_name='O‘lchov birligi', max_length=25, default='kg')
    material_created_date = models.DateTimeField(verbose_name='E‘lon joylangan vaqt', auto_now_add=True)
    material_updated_date = models.DateTimeField(auto_now_add=True, verbose_name='E‘lon tahrirlangan vaqt')
    company_name = models.CharField(verbose_name='Kompaniya', max_length=255, null=True)
    company_stir = models.CharField(verbose_name='Kompaniya STIR', max_length=9, null=True)
    material_region = models.IntegerField(blank=True, null=True)
    material_district = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'all_ads'
