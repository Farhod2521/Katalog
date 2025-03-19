from django.db import models
from django.contrib.auth import get_user_model

from global_vars import measures_mmechano, currency_names

# Create your models here.
class MMechanoCategories(models.Model):
    category_name = models.CharField(max_length=255, verbose_name='Kategoriya nomi (mashina va mexanizmlar)', unique=True)
    category_logo = models.ImageField(max_length=255, verbose_name='Kategoriya logotipi (mashina va mexanizmlar)', default='categories/m-mechano/category_logo.png', upload_to='categories/m-mechano/')
    category_desc = models.CharField(max_length=255, verbose_name='Kategoriya tavsifi (mashina va mexanizmlar)', blank=True, null=True)

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = "mmechano_categories"
        ordering = ['category_name', 'id']


class MMechanoGroups(models.Model):
    group_name = models.CharField(max_length=255, verbose_name='Guruh nomi (mashina va mexanizmlar)', unique=True)
    group_desc = models.CharField(max_length=255, verbose_name='Guruh tavsifi (mashina va mexanizmlar)', blank=True, null=True)
    group_category = models.ForeignKey(MMechanoCategories, on_delete=models.SET_DEFAULT, verbose_name='Guruh kategoriyasi', default=1)

    def __str__(self):
        return self.group_name

    class Meta:
        db_table = "mmechano_groups"
        ordering = ['group_name', 'id']


class MMechano(models.Model):
    mmechano_csr_code = models.CharField(max_length=20, verbose_name='Mashina/mexanizmning klassifikatordagi kodi', primary_key=True)
    mmechano_name = models.CharField(max_length=500, verbose_name='Mashina/mexanizm nomi', unique=True)
    mmechano_desc = models.CharField(max_length=255, verbose_name='Mashina/mexanizm tavsifi', blank=True, null=True)
    mmechano_measure = models.CharField(max_length=25, verbose_name='Mashina/mexanizm o‘lchov birligi', choices=measures_mmechano, default='kg')
    mmechano_group = models.ForeignKey(MMechanoGroups, on_delete=models.SET_DEFAULT, verbose_name='Mashina/mexanizm guruhi', default=1)
    mmechano_image = models.ImageField(verbose_name='Mashina/mexanizm uchun rasm', upload_to='media/m-mechano/', null=True, blank=True)
    mmechano_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)

    def __str__(self):
        return self.mmechano_name

    class Meta:
        db_table = "mmechano_resources"
        ordering = ['mmechano_name', 'mmechano_csr_code']


class MMechanoAllInfo(models.Model):
    mmechano_name = models.CharField(max_length=500)
    mmechano_desc = models.CharField(max_length=255)
    mmechano_measure = models.CharField(max_length=25)
    mmechano_image = models.ImageField(verbose_name='Mashina/mexanizm uchun rasm', upload_to='media/m-mechano/', null=True, blank=True)
    mmechano_csr_code = models.CharField(max_length=20, primary_key=True)
    mmechano_group = models.ForeignKey(MMechanoGroups, on_delete=models.DO_NOTHING)
    mmechano_group_name = models.CharField(max_length=255)
    mmechano_category = models.ForeignKey(MMechanoCategories, on_delete=models.DO_NOTHING)
    mmechano_category_name = models.CharField(max_length=255)
    mmechano_views_count = models.IntegerField(verbose_name='Tashriflar soni', default=0)

    class Meta:
        managed = False
        db_table = 'mmechano_all_infos'


class MMechanoAds(models.Model):
    mmechano_name = models.ForeignKey(MMechano, on_delete=models.DO_NOTHING, verbose_name='Mashina/mexanizm nomi')
    mmechano_description = models.TextField(verbose_name='Mashina/mexanizm tavsifi', max_length=500, blank=True, null=True)
    mmechano_rent_price = models.FloatField(verbose_name='Mashina/mexanizm ijara narxi')
    mmechano_rent_price_currency = models.CharField(verbose_name='Narx ko‘rsatilgan valyuta', choices=currency_names, default='UZS', max_length=15)
    mmechano_measure = models.CharField(verbose_name='Mashina/mexanizm o‘lchov birligi', max_length=25, choices=measures_mmechano, default='kg')
    mmechano_image = models.ImageField(verbose_name='Mashina/mexanizm uchun rasm', upload_to='media/ads/products/', null=True, blank=True)
    mmechano_amount = models.FloatField(verbose_name='Mashina/mexanizm miqdori (Ishlab chiqarish/yetkazib berish qobiliyati)')
    mmechano_amount_measure = models.CharField(verbose_name='O‘lchov birligi', max_length=25, choices=measures_mmechano, default='kg')
    mmechano_status = models.BooleanField(verbose_name='E‘lon holati', default=True)
    mmechano_created_date = models.DateTimeField(verbose_name='E‘lon joylangan vaqt', auto_now_add=True)
    mmechano_updated_date = models.DateTimeField(auto_now_add=True, verbose_name='E‘lon tahrirlangan vaqt')
    mmechano_deactivated_date = models.DateTimeField(verbose_name='E‘lon o‘chirilgan vaqt', blank=True, null=True)
    # mmechano_views_count = models.IntegerField(verbose_name='E‘lonni ko‘rishlar soni', default=0)
    # mmechano_company = # Set after creating model for Companies
    sertificate_blank_num = models.CharField(verbose_name='Mashina/mexanizm sertifikat blanka raqami', max_length=10)
    sertificate_reestr_num = models.CharField(verbose_name='Mashina/mexanizm sertifikat reestr raqami', max_length=10)
    mmechano_owner = models.ForeignKey(get_user_model(), verbose_name='E‘lon muallifi', on_delete=models.CASCADE)
    company_name = models.CharField(verbose_name='Kompaniya', max_length=255, null=True)
    company_stir = models.CharField(verbose_name='Kompaniya STIR', max_length=9, null=True)

    class Meta:
        db_table = 'mmechano_ads'

    def __str__(self):
        return str(self.mmechano_name)


class MMechnoAdExcel(models.Model):
    mmechano_name  =  models.CharField(max_length=300, verbose_name="Nomi")
    mmechano_measure =  models.CharField(max_length=30, verbose_name="O'lchov birligi")
    mmechno_price =  models.PositiveIntegerField()


    class Meta:
        db_table = 'mmechano_excel'

    def __str__(self) -> str:
        return self.mmechano_name

