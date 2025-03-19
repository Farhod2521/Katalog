from django.db import models
from django.contrib.auth import get_user_model

from global_vars import measures_works, currency_names

# Create your models here.
class WorkCategories(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Kategoriya nomi (qurilish ishlari)', unique=True)
    category_logo = models.ImageField(max_length=255, verbose_name='Kategoriya logotipi (qurilish ishlari)', default='categories/works/category_logo.png', upload_to='categories/works/')
    category_desc = models.CharField(max_length=255, verbose_name='Kategoriya tavsifi (qurilish ishlari)', blank=True, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "work_categories"
        ordering = ['category_name', 'id']


class WorkGroups(models.Model):
    group_name = models.CharField(max_length=255, verbose_name='Guruh nomi (qurilish ishlari)', unique=True)
    group_desc = models.CharField(max_length=255, verbose_name='Guruh tavsifi (qurilish ishlari)', blank=True, null=True)
    group_category = models.ForeignKey(WorkCategories, on_delete=models.SET_DEFAULT, verbose_name='Guruh kategoriyasi', default=1)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = "work_groups"
        ordering = ['group_name', 'id']


class Work(models.Model):
    work_csr_code = models.CharField(max_length=20, verbose_name='Qurilish ishining klassifikatordagi kodi', primary_key=True)
    work_name = models.CharField(max_length=500, verbose_name='Qurilish ishi nomi', unique=True)
    work_desc = models.CharField(max_length=255, verbose_name='Qurilish ishi tavsifi', blank=True, null=True)
    work_measure = models.CharField(max_length=25, verbose_name='Qurilish ishi o‘lchov birligi', choices=measures_works, default='kg')
    work_group = models.ForeignKey(WorkGroups, on_delete=models.SET_DEFAULT, verbose_name='Qurilish ishi guruhi', default=1)
    work_image = models.ImageField(verbose_name='Ish turi uchun rasm', upload_to='media/works/', null=True, blank=True)
    work_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)

    def __str__(self):
        return self.work_name

    class Meta:
        db_table = "work_resources"
        ordering = ['work_name', 'work_csr_code']


class WorkAllInfo(models.Model):
    work_name = models.CharField(max_length=500)
    work_desc = models.CharField(max_length=255)
    work_measure = models.CharField(max_length=25)
    work_csr_code = models.CharField(max_length=20, primary_key=True)
    work_image = models.ImageField(verbose_name='Ish turi uchun rasm', upload_to='media/works/', null=True, blank=True)
    work_group = models.ForeignKey(WorkGroups, on_delete=models.DO_NOTHING)
    work_group_name = models.CharField(max_length=255)
    work_category = models.ForeignKey(WorkCategories, on_delete=models.DO_NOTHING)
    work_category_name = models.CharField(max_length=255)
    work_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)

    class Meta:
        managed = False
        db_table = 'work_all_infos'


class WorkAds(models.Model):
    work_name = models.ForeignKey(Work, on_delete=models.SET_DEFAULT, verbose_name='Qurilish ishi nomi', default=1)
    work_description = models.TextField(verbose_name='Qurilish ishi tavsifi', max_length=500, blank=True, null=True)
    work_rent_price = models.FloatField(verbose_name='Qurilish ishi ijara narxi')
    work_rent_price_currency = models.CharField(verbose_name='Narx ko‘rsatilgan valyuta', choices=currency_names, default='UZS', max_length=15)
    work_measure = models.CharField(verbose_name='Qurilish ishi o‘lchov birligi', max_length=25, choices=measures_works, default='kg')
    work_image = models.ImageField(verbose_name='Qurilish ishi uchun rasm', upload_to='media/ads/products/', null=True, blank=True)
    work_amount = models.FloatField(verbose_name='Qurilish ishi miqdori (Ishlab chiqarish/yetkazib berish qobiliyati)')
    work_amount_measure = models.CharField(verbose_name='O‘lchov birligi', max_length=25, choices=measures_works, default='dona')
    work_status = models.BooleanField(verbose_name='E‘lon holati', default=True)
    work_created_date = models.DateTimeField(verbose_name='E‘lon joylangan vaqt', auto_now_add=True)
    work_updated_date = models.DateTimeField(auto_now_add=True, verbose_name='E‘lon tahrirlangan vaqt')
    work_deactivated_date = models.DateTimeField(verbose_name='E‘lon o‘chirilgan vaqt', blank=True, null=True)
    # work_views_count = models.IntegerField(verbose_name='E‘lonni ko‘rishlar soni', default=0)
    # work_company = # Set after creating model for Companies
    sertificate_blank_num = models.CharField(verbose_name='Qurilish ishi sertifikat blanka raqami', max_length=10)
    sertificate_reestr_num = models.CharField(verbose_name='Qurilish ishi sertifikat reestr raqami', max_length=10)
    work_owner = models.ForeignKey(get_user_model(), verbose_name='E‘lon muallifi', on_delete=models.CASCADE)
    company_name = models.CharField(verbose_name='Kompaniya', max_length=255, null=True)
    company_stir = models.CharField(verbose_name='Kompaniya STIR', max_length=9, null=True)

    class Meta:
        db_table = 'work_ads'

    def __str__(self):
        return self.work_name