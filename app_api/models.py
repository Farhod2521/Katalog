from django.db import models
from django.contrib.auth import get_user_model

# from app_company.models import Companies




class Material_Soliq_Price(models.Model):
    material_csr_code = models.CharField(max_length=200)
    material_name =  models.CharField(max_length=200)
    mxik_code  =  models.CharField(max_length=200)
    material_measure =  models.CharField(max_length=20)

    def __str__(self):
        return self.material_name
    
    class Meta:
        db_table = 'material_soliq_price'


class Document_Category(models.Model):
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'document_category'


class Document(models.Model):
    category =  models.ForeignKey(Document_Category, on_delete=models.CASCADE)
    title  = models.CharField(max_length=500)
    file   =  models.FileField(upload_to="HUjjat/")

    class Meta:
        db_table = 'document'


# Create your models here.
class CustomLanguages(models.Model):
    key_name = models.CharField(max_length=25, verbose_name="Kalit so‘z", unique=True)
    uz = models.CharField(max_length=255, verbose_name="O‘zbek", unique=True)
    en = models.CharField(max_length=255, verbose_name="English", unique=True, null=True)
    ru = models.CharField(max_length=255, verbose_name="Русский", unique=True, null=True)
    
    def __str__(self):
        return self.key_name

    class Meta:
        db_table = 'lang_translations'
        # ordering = ['volume_code', 'volume_name']


class SelectedThings(models.Model):
    user = models.ForeignKey(get_user_model(), verbose_name='User', on_delete=models.DO_NOTHING)
    thing_id = models.CharField(max_length=25, verbose_name='Selected thing (company, product, ad) ID')
    thing_types = {
        ('C', 'company'),
        ('M', 'material'),
        ('MM', 'm_mechano'),
        ('SM', 'small_mechano'),
        ('T', 'techno'),
        ('W', 'work'),
        ('A', 'ad'),
    }
    thing_type = models.CharField(choices=thing_types, verbose_name='Thing type', max_length=2)
    selected_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Selected time')
    deselected = models.BooleanField(verbose_name='Selection canceled', default=0)
    deselected_time = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Deselected time', null=True)
    
    def __str__(self):
        return self.thing_id

    class Meta:
        db_table = 'selected_things'



class ResourcesList4Search(models.Model):
    resource_name = models.CharField(max_length=500)
    resource_code = models.CharField(max_length=20, primary_key=True)
    resource_desc = models.TextField(null=True, blank=True)
    resource_image = models.ImageField(verbose_name='Resurs uchun rasm', upload_to='media/', null=True, blank=True)
    resource_url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'resources'




class Birja_Week(models.Model):
    old_monday = models.DateField(auto_now=False)
    old_friday = models.DateField(auto_now=False)





class BojxonaCategory(models.Model):
    bj_id =  models.CharField(max_length=50, default="1900bb05d0d_1_ugtd")
    date =  models.DateTimeField(auto_now=True)
    get15 = models.CharField(max_length=200, null=True, blank=True)
    error =  models.CharField(max_length=200, null=True, blank=True)
    class Meta:
        db_table = 'bojxona_catgory'

class Bojxona(models.Model):
    bj_category=models.ForeignKey(BojxonaCategory, on_delete=models.CASCADE)
    unit = models.CharField(max_length=200, blank=True, null=True)
    codeName = models.CharField(max_length=1000)
    additionalUnit = models.FloatField(max_length=20)
    codeTiftn = models.CharField(max_length=200)
    g31name = models.CharField(max_length=1000, blank=True, null=True)
    value = models.FloatField(max_length=20)
    netMass = models.FloatField(max_length=20)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.codeName
    class Meta:
        db_table = 'bojxona'

class TexnikJTSACategory(models.Model):
    year  =  models.PositiveIntegerField()
    class Meta:
        db_table = 'texnik_jtsa_catgory'

class TexnikJTSA(models.Model):
    year =  models.ForeignKey(TexnikJTSACategory, on_delete=models.CASCADE)
    name  =  models.CharField(max_length=300)
    gost =  models.CharField(max_length=500)
    sxema =  models.CharField(max_length=50)
    company_name =  models.CharField(max_length=300)
    company_stir =  models.IntegerField(null=True, blank=True)
    country =  models.CharField(max_length=200)
    price =  models.FloatField()

    def __str__(self) -> str:
        return self.name
    class Meta:
        db_table = 'texnik_jtsa'



class Iqtisod_Moliya(models.Model):
    productPrice =  models.IntegerField()
    productName =  models.CharField(max_length=300)
    productCode =  models.CharField(max_length=200)
    inn =  models.IntegerField()
    company_name = models.CharField(max_length=200, blank=True, null=True)
    lot_Date =  models.DateField(auto_now=True)

    class Meta:
        db_table = 'iqtisod_moliya'

    def __str__(self) -> str:
        return self.productName
