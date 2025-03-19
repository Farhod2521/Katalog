from django.db import models
from django.contrib.auth import get_user_model

from global_vars import measures_product, currency_names

# Create your models here.
class ProductVolumes(models.Model):
    volume_name = models.CharField(max_length=255, verbose_name='Bo‘lim nomi (qurilish buyumlari)', unique=True)
    volume_logo = models.ImageField(max_length=255, verbose_name='Bo‘lim logotipi (qurilish buyumlari)', default='static/categories/products/volume_logo.png', upload_to='categories/products/')
    volume_desc = models.CharField(max_length=255, verbose_name='Bo‘lim tavsifi (qurilish buyumlari)', blank=True, null=True)

    def __str__(self):
        return self.volume_name

    class Meta:
        db_table = "product_volumes"
        ordering = ['volume_name', 'id']


class ProductCategories(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Kategoriya nomi (qurilish buyumlari)', unique=True)
    category_desc = models.CharField(max_length=255, verbose_name='Kategoriya tavsifi (qurilish buyumlari)', blank=True, null=True)
    category_volume = models.ForeignKey(ProductVolumes, on_delete=models.SET_DEFAULT, verbose_name='Kategoriya bo‘limi', default=1)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "product_categories"
        ordering = ['category_name', 'id']


class ProductGroups(models.Model):
    group_name = models.CharField(max_length=255, verbose_name='Guruh nomi (qurilish buyumlari)', unique=True)
    group_desc = models.CharField(max_length=255, verbose_name='Guruh tavsifi (qurilish buyumlari)', blank=True, null=True)
    group_category = models.ForeignKey(ProductCategories, on_delete=models.SET_DEFAULT, verbose_name='Guruh kategoriyasi', default=1)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = "product_groups"
        ordering = ['group_name', 'id']


class Product(models.Model):
    product_csr_code = models.CharField(max_length=20, verbose_name='Qurilish buyumining klassifikatordagi kodi', primary_key=True)
    product_name = models.CharField(max_length=500, verbose_name='Qurilish buyumi nomi', unique=True)
    product_desc = models.CharField(max_length=255, verbose_name='Qurilish buyumi tavsifi', blank=True, null=True)
    product_measure = models.CharField(max_length=25, verbose_name='Qurilish buyumi o‘lchov birligi', choices=measures_product, default='kg')
    product_group = models.ForeignKey(ProductGroups, on_delete=models.SET_DEFAULT, verbose_name='Qurilish buyumi guruhi', default=1)
    product_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = "product_resources"
        ordering = ['product_name', 'product_csr_code']


class ProductAllInfo(models.Model):
    product_name = models.CharField(max_length=500)
    product_desc = models.CharField(max_length=255)
    product_measure = models.CharField(max_length=25)
    product_csr_code = models.CharField(max_length=20, primary_key=True)
    product_group = models.ForeignKey(ProductGroups, on_delete=models.DO_NOTHING)
    product_group_name = models.CharField(max_length=255)
    product_category = models.ForeignKey(ProductCategories, on_delete=models.DO_NOTHING)
    product_category_name = models.CharField(max_length=255)
    product_volume = models.ForeignKey(ProductVolumes, on_delete=models.DO_NOTHING)
    product_volume_name = models.CharField(max_length=255)
    product_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)

    class Meta:
        managed = False
        db_table = 'product_all_infos'


class ProductAds(models.Model):
    product_name = models.ForeignKey(Product, on_delete=models.SET_DEFAULT, verbose_name='Qurilish buyumi nomi', default=1)
    product_description = models.TextField(verbose_name='Qurilish buyumi tavsifi', max_length=500, blank=True, null=True)
    product_price = models.FloatField(verbose_name='Qurilish buyumi narxi')
    product_price_currency = models.CharField(verbose_name='Narx ko‘rsatilgan valyuta', choices=currency_names, default='UZS', max_length=15)
    product_measure = models.CharField(verbose_name='Qurilish buyumi o‘lchov birligi', max_length=25, choices=measures_product, default='kg')
    product_image = models.ImageField(verbose_name='Qurilish buyumi uchun rasm', upload_to='media/ads/products/', null=True, blank=True)
    product_amount = models.FloatField(verbose_name='Qurilish buyumi miqdori (Ishlab chiqarish/yetkazib berish qobiliyati)')
    product_amount_measure = models.CharField(verbose_name='O‘lchov birligi', max_length=25, choices=measures_product, default='kg')
    product_status = models.BooleanField(verbose_name='E‘lon holati', default=True)
    product_created_date = models.DateTimeField(verbose_name='E‘lon joylangan vaqt', auto_now_add=True)
    product_updated_date = models.DateTimeField(auto_now_add=True, verbose_name='E‘lon tahrirlangan vaqt')
    product_deactivated_date = models.DateTimeField(verbose_name='E‘lon o‘chirilgan vaqt', blank=True, null=True)
    # product_views_count = models.IntegerField(verbose_name='E‘lonni ko‘rishlar soni', default=0)
    # product_company = # Set after creating model for Companies
    sertificate_blank_num = models.CharField(verbose_name='Qurilish buyumi sertifikat blanka raqami', max_length=10)
    sertificate_reestr_num = models.CharField(verbose_name='Qurilish buyumi sertifikat reestr raqami', max_length=10)
    product_owner = models.ForeignKey(get_user_model(), verbose_name='E‘lon muallifi', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_ads'

    def __str__(self):
        return self.product_name