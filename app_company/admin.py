from django.contrib import admin
from .models import Companies
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class CompanyAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['company_stir', 'company_name', 'company_phone_main', 'company_region', 'company_district', 'company_email', 'company_ceo']
    list_filter = ['company_region', 'company_district']
    search_fields = ['company_stir', 'company_name']

admin.site.register(Companies, CompanyAdmin)
