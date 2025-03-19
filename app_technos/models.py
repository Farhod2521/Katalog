from django.db import models
from django.contrib.auth import get_user_model

from app_company.models import Regions, Districts

from global_vars import measures_techno, currency_names

# Create your models here.
class TechnoVolumes(models.Model):
    volume_name = models.CharField(max_length=255, verbose_name='Bo‘lim nomi (texnika)', unique=True)
    volume_logo = models.ImageField(max_length=255, verbose_name='Bo‘lim logotipi (texnika)', default='static/categories/technos/volume_logo.png', upload_to='categories/technos/')
    volume_desc = models.CharField(max_length=255, verbose_name='Bo‘lim tavsifi (texnika)', blank=True, null=True)

    def __str__(self):
        return self.volume_name

    class Meta:
        db_table = "techno_volumes"
        ordering = ['volume_name', 'id']


class TechnoCategories(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Kategoriya nomi (texnika)', unique=True)
    category_desc = models.CharField(max_length=255, verbose_name='Kategoriya tavsifi (texnika)', blank=True, null=True)
    category_volume = models.ForeignKey(TechnoVolumes, on_delete=models.SET_DEFAULT, verbose_name='Kategoriya bo‘limi', default=1)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "techno_categories"
        ordering = ['category_name', 'id']


class TechnoGroups(models.Model):
    group_name = models.CharField(max_length=255, verbose_name='Guruh nomi (texnika)', unique=True)
    group_desc = models.CharField(max_length=255, verbose_name='Guruh tavsifi (texnika)', blank=True, null=True)
    group_category = models.ForeignKey(TechnoCategories, on_delete=models.SET_DEFAULT, verbose_name='Guruh kategoriyasi', default=1)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = "techno_groups"
        ordering = ['group_name', 'id']


class Techno(models.Model):
    techno_csr_code = models.CharField(max_length=20, verbose_name='Texnikaning klassifikatordagi kodi', primary_key=True)
    techno_name = models.CharField(max_length=500, verbose_name='Texnika nomi', unique=True)
    techno_desc = models.CharField(max_length=255, verbose_name='Texnika tavsifi', blank=True, null=True)
    techno_measure = models.CharField(max_length=25, verbose_name='Texnika o‘lchov birligi', choices=measures_techno, default='kg')
    techno_group = models.ForeignKey(TechnoGroups, on_delete=models.SET_DEFAULT, verbose_name='Texnika guruhi', default=1)
    techno_image = models.ImageField(verbose_name='Qurilma/jihoz uchun rasm', upload_to='technos/', null=True, blank=True)
    techno_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)

    def __str__(self):
        return self.techno_name

    class Meta:
        db_table = "techno_resources"
        ordering = ['techno_name', 'techno_csr_code']


class TechnoAllInfo(models.Model):
    techno_name = models.CharField(max_length=500)
    techno_desc = models.CharField(max_length=255)
    techno_measure = models.CharField(max_length=25)
    techno_csr_code = models.CharField(max_length=20, primary_key=True)
    techno_image = models.ImageField(verbose_name='Qurilma/jihoz uchun rasm', upload_to='technos/', null=True, blank=True)
    techno_group = models.ForeignKey(TechnoGroups, on_delete=models.DO_NOTHING)
    techno_group_name = models.CharField(max_length=255)
    techno_category = models.ForeignKey(TechnoCategories, on_delete=models.DO_NOTHING)
    techno_category_name = models.CharField(max_length=255)
    techno_volume = models.ForeignKey(TechnoVolumes, on_delete=models.DO_NOTHING)
    techno_volume_name = models.CharField(max_length=255)
    techno_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)

    class Meta:
        managed = False
        db_table = 'techno_all_infos'


class TechnoAds(models.Model):
    techno_name = models.ForeignKey(Techno, on_delete=models.DO_NOTHING, verbose_name='Texnika nomi')
    techno_description = models.TextField(verbose_name='Texnika tavsifi', max_length=500, blank=True, null=True)
    techno_price = models.FloatField(verbose_name='Texnika narxi')
    techno_price_currency = models.CharField(verbose_name='Narx ko‘rsatilgan valyuta', choices=currency_names, default='UZS', max_length=15)
    techno_measure = models.CharField(verbose_name='Texnika o‘lchov birligi', max_length=25)
    techno_image = models.ImageField(verbose_name='Texnika uchun rasm', upload_to='ads/technos/', null=True, blank=True)
    techno_amount = models.FloatField(verbose_name='Texnika miqdori (Ishlab chiqarish/yetkazib berish qobiliyati)')
    techno_amount_measure = models.CharField(verbose_name='O‘lchov birligi', max_length=25)
    techno_status = models.BooleanField(verbose_name='E‘lon holati', default=True)
    techno_created_date = models.DateTimeField(verbose_name='E‘lon joylangan vaqt', auto_now_add=True)
    techno_updated_date = models.DateTimeField(auto_now_add=True, verbose_name='E‘lon tahrirlangan vaqt')
    techno_deactivated_date = models.DateTimeField(verbose_name='E‘lon o‘chirilgan vaqt', blank=True, null=True)
    # techno_views_count = models.IntegerField(verbose_name='E‘lonni ko‘rishlar soni', default=0)
    # techno_company = # Set after creating model for Companies
    sertificate_blank_num = models.CharField(verbose_name='Texnika sertifikat blanka raqami', max_length=10)
    sertificate_reestr_num = models.CharField(verbose_name='Texnika sertifikat reestr raqami', max_length=10)
    techno_owner = models.ForeignKey(get_user_model(), verbose_name='E‘lon muallifi', on_delete=models.CASCADE)
    company_name = models.CharField(verbose_name='Kompaniya', max_length=255, null=True)
    company_stir = models.CharField(verbose_name='Kompaniya STIR', max_length=9, null=True)
    techno_region = models.ForeignKey(Regions, on_delete=models.SET_NULL, verbose_name='Viloyat', blank=True, null=True)
    techno_district = models.ForeignKey(Districts, on_delete=models.SET_NULL, verbose_name='Tuman/shahar', blank=True, null=True)

    class Meta:
        db_table = 'techno_ads'

    def __str__(self):
        return str(self.techno_name)
