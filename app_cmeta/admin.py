from django.contrib import admin
from .models import Cmeta, CmetaCategory, Sample_Project
# Register your models here.
from import_export.admin import ImportExportModelAdmin

class CmetaAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id', 'name', 'code']



admin.site.register(Cmeta, CmetaAdmin)
admin.site.register(CmetaCategory)


class Sample_ProjectAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id', 'name', 'code']



admin.site.register(Sample_Project, Sample_ProjectAdmin)
