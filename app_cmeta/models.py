from django.db import models

# Create your models here.
class CmetaCategory(models.Model):
    name  =  models.CharField(max_length=200)


    class Meta:
        db_table = 'cmeta_category'


class Cmeta(models.Model):
    category =  models.ForeignKey(CmetaCategory, on_delete=models.CASCADE)
    name =  models.CharField(max_length=300)
    code =  models.CharField(max_length=100)
    measure =  models.CharField(max_length=10)
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'cmeta'
    


class Sample_ProjectCategory(models.Model):
    name  =  models.CharField(max_length=200)


    class Meta:
        db_table = 'sample_project_category'


class Sample_Project(models.Model):
    category =  models.ForeignKey(Sample_ProjectCategory, on_delete=models.CASCADE)
    name =  models.CharField(max_length=300)
    code =  models.CharField(max_length=100)
    measure =  models.CharField(max_length=10)
    price =  models.CharField(blank=True, null=True, max_length=100)
    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = 'sample_project'
    
