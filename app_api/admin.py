from django.contrib import admin

from .models import Birja_Week, Bojxona, BojxonaCategory, TexnikJTSACategory, TexnikJTSA, Iqtisod_Moliya
from import_export.admin import ImportExportModelAdmin

admin.site.register(Birja_Week)
admin.site.register(Bojxona)
admin.site.register(BojxonaCategory)

class IQTISODAExcelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['productName', 'productCode']
admin.site.register(Iqtisod_Moliya, IQTISODAExcelAdmin)


admin.site.register(TexnikJTSACategory)
class TexnikJTSAExcelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['name', 'gost', 'price']
  
admin.site.register(TexnikJTSA, TexnikJTSAExcelAdmin)


# Register your models here.
