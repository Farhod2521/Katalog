from django.db import models
from django.contrib.auth import get_user_model

from app_company.models import Regions, Districts

from global_vars import measures, currency_names

# Create your models here.
class MatVolumes(models.Model):
    volume_name = models.CharField(max_length=255, verbose_name='Bo‘lim nomi (material)', unique=True)
    volume_logo = models.ImageField(max_length=255, verbose_name='Bo‘lim logotipi (material)', default='static/categories/materials/volume_logo.png', upload_to='categories/materials/')
    volume_desc = models.CharField(max_length=255, verbose_name='Bo‘lim tavsifi (material)', blank=True, null=True)

    def __str__(self):
        return self.volume_name

    class Meta:
        db_table = "material_volumes"
        ordering = ['volume_name', 'id']


class MatCategories(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Kategoriya nomi (material)', unique=True)
    category_desc = models.CharField(max_length=255, verbose_name='Kategoriya tavsifi (material)', blank=True, null=True)
    category_volume = models.ForeignKey(MatVolumes, on_delete=models.SET_DEFAULT, verbose_name='Kategoriya bo‘limi', default=1)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "material_categories"
        ordering = ['category_name', 'id']


class MatGroups(models.Model):
    group_name = models.CharField(max_length=255, verbose_name='Guruh nomi (material)', unique=True)
    group_desc = models.CharField(max_length=255, verbose_name='Guruh tavsifi (material)', blank=True, null=True)
    group_category = models.ForeignKey(MatCategories, on_delete=models.SET_DEFAULT, verbose_name='Guruh kategoriyasi', default=1)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = "material_groups"
        ordering = ['group_name', 'id']


class Materials(models.Model):
    material_csr_code = models.CharField(max_length=20, verbose_name='Materialning klassifikatordagi kodi', primary_key=True)
    material_name = models.CharField(max_length=1500, verbose_name='Material nomi')
    material_desc = models.CharField(max_length=255, verbose_name='Material tavsifi', blank=True, null=True)
    material_measure = models.CharField(max_length=25, verbose_name='Material o‘lchov birligi', choices=measures, default='kg')
    material_group = models.ForeignKey(MatGroups, on_delete=models.SET_DEFAULT, verbose_name='Material guruhi', default=1)
    material_image = models.ImageField(verbose_name='Material uchun rasm', upload_to='materials/', null=True, blank=True)
    material_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)
    materil_gost =  models.CharField(max_length=255, verbose_name='Material GOST', blank=True, null=True)
    def __str__(self):
        return self.material_name

    class Meta:
        db_table = "material_resources"
        ordering = ['material_name', 'material_csr_code']


class MaterialsAllInfo(models.Model):
    material_name = models.CharField(max_length=1500)
    material_desc = models.CharField(max_length=255)
    material_measure = models.CharField(max_length=25)
    material_csr_code = models.CharField(max_length=20, primary_key=True)
    material_image = models.ImageField(verbose_name='Material uchun rasm', upload_to='media/materials/', null=True, blank=True)
    material_group = models.ForeignKey(MatGroups, on_delete=models.DO_NOTHING)
    material_group_name = models.CharField(max_length=255)
    material_category = models.ForeignKey(MatCategories, on_delete=models.DO_NOTHING)
    material_category_name = models.CharField(max_length=255)
    material_volume = models.ForeignKey(MatVolumes, on_delete=models.DO_NOTHING)
    material_volume_name = models.CharField(max_length=255)
    material_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)

    class Meta:
        #managed = False
        db_table = 'material_all_infos'


class MaterialAds(models.Model):
    material_name = models.ForeignKey(Materials, on_delete=models.DO_NOTHING, verbose_name='Material nomi')
    material_description = models.TextField(verbose_name='Material tavsifi', max_length=500, blank=True, null=True)
    material_price = models.FloatField(verbose_name='Material narxi')
    material_price_currency = models.CharField(verbose_name='Narx ko‘rsatilgan valyuta', choices=currency_names, default='UZS', max_length=15)
    material_measure = models.CharField(verbose_name='Material o‘lchov birligi', max_length=25)
    material_image = models.ImageField(verbose_name='Material uchun rasm', upload_to='ads/materials/', null=True, blank=True)
    material_amount = models.FloatField(verbose_name='Material miqdori (Ishlab chiqarish/yetkazib berish qobiliyati)')
    material_amount_measure = models.CharField(verbose_name='O‘lchov birligi', max_length=25)
    material_status = models.BooleanField(verbose_name='E‘lon holati', default=True)
    material_created_date = models.DateTimeField(verbose_name='E‘lon joylangan vaqt', auto_now_add=True)
    material_updated_date = models.DateTimeField(auto_now_add=True, verbose_name='E‘lon tahrirlangan vaqt')
    material_deactivated_date = models.DateTimeField(verbose_name='E‘lon o‘chirilgan vaqt', blank=True, null=True)
    # material_views_count = models.IntegerField(verbose_name='E‘lonni ko‘rishlar soni', default=0)
    # material_company = # Set after creating model for Companies
    sertificate_blank_num = models.CharField(verbose_name='Maxsulot sertifikat blanka raqami', max_length=25)
    sertificate_reestr_num = models.CharField(verbose_name='Maxsulot sertifikat reestr raqami', max_length=25)
    material_owner = models.ForeignKey(get_user_model(), verbose_name='E‘lon muallifi', on_delete=models.CASCADE)
    company_name = models.CharField(verbose_name='Kompaniya', max_length=255, null=True)
    company_stir = models.CharField(verbose_name='Kompaniya STIR', max_length=9, null=True)
    material_region = models.ForeignKey(Regions, on_delete=models.SET_NULL, verbose_name='Viloyat', blank=True, null=True)
    material_district = models.ForeignKey(Districts, on_delete=models.SET_NULL, verbose_name='Tuman/shahar', blank=True, null=True)

    	
    
    class Meta:
        db_table = 'material_ads'
    def __str__(self):
        return str(self.material_name)


