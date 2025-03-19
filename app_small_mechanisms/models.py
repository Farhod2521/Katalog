from django.db import models
from django.contrib.auth import get_user_model

from global_vars import measures_mmechano, currency_names

# Create your models here.
class SmallMechanoCategories(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Kategoriya nomi (kichik mexanizmlar)', unique=True)
    category_logo = models.ImageField(max_length=255, verbose_name='Kategoriya logotipi (kichik mexanizmlar)', default='categories/small-mechano/category_logo.png', upload_to='categories/small-mechano/')
    category_desc = models.CharField(max_length=255, verbose_name='Kategoriya tavsifi (kichik mexanizmlar)', blank=True, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "smallmechano_categories"
        ordering = ['category_name', 'id']


class SmallMechanoGroups(models.Model):
    group_name = models.CharField(max_length=255, verbose_name='Guruh nomi (kichik mexanizmlar)', unique=True)
    group_desc = models.CharField(max_length=255, verbose_name='Guruh tavsifi (kichik mexanizmlar)', blank=True, null=True)
    group_category = models.ForeignKey(SmallMechanoCategories, on_delete=models.SET_DEFAULT, verbose_name='Guruh kategoriyasi', default=1)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = "smallmechano_groups"
        ordering = ['group_name', 'id']


class SmallMechano(models.Model):
    smallmechano_csr_code = models.CharField(max_length=20, verbose_name='Kichik mexanizmning klassifikatordagi kodi', primary_key=True)
    smallmechano_name = models.CharField(max_length=500, verbose_name='Kichik mexanizm nomi', unique=True)
    smallmechano_desc = models.CharField(max_length=255, verbose_name='Kichik mexanizm tavsifi', blank=True, null=True)
    smallmechano_measure = models.CharField(max_length=25, verbose_name='Kichik mexanizm o‘lchov birligi', choices=measures_mmechano, default='kg')
    smallmechano_group = models.ForeignKey(SmallMechanoGroups, on_delete=models.SET_DEFAULT, verbose_name='Kichik mexanizm guruhi', default=1)
    smallmechano_image = models.ImageField(verbose_name='Kichik mexanizatsiya uchun rasm', upload_to='media/small-mechano/', null=True, blank=True)
    smallmechano_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)

    def __str__(self):
        return self.smallmechano_name

    class Meta:
        db_table = "smallmechano_resources"
        ordering = ['smallmechano_name', 'smallmechano_csr_code']


class SmallMechanoAllInfo(models.Model):
    smallmechano_name = models.CharField(max_length=500)
    smallmechano_desc = models.CharField(max_length=255)
    smallmechano_measure = models.CharField(max_length=25)
    smallmechano_csr_code = models.CharField(max_length=20, primary_key=True)
    smallmechano_image = models.ImageField(verbose_name='Kichik mexanizatsiya uchun rasm', upload_to='media/small-mechano/', null=True, blank=True)
    smallmechano_group = models.ForeignKey(SmallMechanoGroups, on_delete=models.DO_NOTHING)
    smallmechano_group_name = models.CharField(max_length=255)
    smallmechano_category = models.ForeignKey(SmallMechanoCategories, on_delete=models.DO_NOTHING)
    smallmechano_category_name = models.CharField(max_length=255)
    smallmechano_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)

    class Meta:
        managed = False
        db_table = 'smallmechano_all_infos'


class SmallMechanoAds(models.Model):
    smallmechano_name = models.ForeignKey(SmallMechano, on_delete=models.DO_NOTHING, verbose_name='Kichik mexanizm nomi')
    smallmechano_description = models.TextField(verbose_name='Kichik mexanizm tavsifi', max_length=500, blank=True, null=True)
    smallmechano_rent_price = models.FloatField(verbose_name='Kichik mexanizm ijara narxi')
    smallmechano_rent_price_currency = models.CharField(verbose_name='Narx ko‘rsatilgan valyuta', choices=currency_names, default='UZS', max_length=15)
    smallmechano_measure = models.CharField(verbose_name='Kichik mexanizm o‘lchov birligi', max_length=25, choices=measures_mmechano, default='kg')
    smallmechano_image = models.ImageField(verbose_name='Kichik mexanizm uchun rasm', upload_to='media/ads/products/', null=True, blank=True)
    smallmechano_amount = models.FloatField(verbose_name='Kichik mexanizm miqdori (Ishlab chiqarish/yetkazib berish qobiliyati)')
    smallmechano_amount_measure = models.CharField(verbose_name='O‘lchov birligi', max_length=25, choices=measures_mmechano, default='kg')
    smallmechano_status = models.BooleanField(verbose_name='E‘lon holati', default=True)
    smallmechano_created_date = models.DateTimeField(verbose_name='E‘lon joylangan vaqt', auto_now_add=True)
    smallmechano_updated_date = models.DateTimeField(auto_now_add=True, verbose_name='E‘lon tahrirlangan vaqt')
    smallmechano_deactivated_date = models.DateTimeField(verbose_name='E‘lon o‘chirilgan vaqt', blank=True, null=True)
    # smallmechano_views_count = models.IntegerField(verbose_name='E‘lonni ko‘rishlar soni', default=0)
    # smallmechano_company = # Set after creating model for Companies
    sertificate_blank_num = models.CharField(verbose_name='Kichik mexanizm sertifikat blanka raqami', max_length=10)
    sertificate_reestr_num = models.CharField(verbose_name='Kichik mexanizm sertifikat reestr raqami', max_length=10)
    smallmechano_owner = models.ForeignKey(get_user_model(), verbose_name='E‘lon muallifi', on_delete=models.CASCADE)
    company_name = models.CharField(verbose_name='Kompaniya', max_length=255, null=True)
    company_stir = models.CharField(verbose_name='Kompaniya STIR', max_length=9, null=True)

    class Meta:
        db_table = 'smallmechano_ads'

    def __str__(self):
        return str(self.smallmechano_name)
