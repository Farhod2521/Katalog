from django.contrib import admin

from .models import MMechanoCategories, MMechanoGroups, MMechano, MMechanoAds, MMechnoAdExcel

# Register your models here.
# admin.site.register(MMechanoCategories)
# admin.site.register(MMechanoGroups)
# admin.site.register(MMechano)
# admin.site.register(MMechanoAds)

from import_export.admin import ImportExportModelAdmin



class MMechnoAdExcelAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['mmechano_name', 'mmechano_measure', 'mmechno_price']
  
admin.site.register(MMechnoAdExcel, MMechnoAdExcelAdmin)


# Register MMechanoerialAds Admin
class MMechanoAdsAdmin(admin.ModelAdmin):
    list_display = ['id', 'mmechano_name', 'mmechano_description', 'mmechano_owner', 'company_stir']
    list_filter = ['mmechano_name', 'mmechano_description', 'mmechano_owner', 'company_stir']
    # search_fields = ['mmechano_name', 'mmechano_description']

admin.site.register(MMechanoAds, MMechanoAdsAdmin)


# Register MMechanoCategories Admin
class MMechanoCategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'category_desc']
    ordering = ('id',)
    # search_fields = ['mmechano_name', 'mmechano_description']

admin.site.register(MMechanoCategories, MMechanoCategoriesAdmin)


# Register MMechanoCategories Admin
class MMechanoGroupsAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name', 'group_desc', 'group_category']
    list_filter = ['group_category']
    ordering = ('id', 'group_category')
    # search_fields = ['mmechano_name', 'mmechano_description']

admin.site.register(MMechanoGroups, MMechanoGroupsAdmin)


# Register MMechanoCategories Admin
class MMechanoAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['mmechano_csr_code', 'mmechano_name', 'mmechano_measure', 'mmechano_image', 'mmechano_group']
    list_filter = ['mmechano_measure', 'mmechano_group']
    ordering = ('mmechano_group', 'mmechano_name')
    search_fields = ['mmechano_name', 'mmechano_csr_code']

admin.site.register(MMechano, MMechanoAdmin)
