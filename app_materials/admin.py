from django.contrib import admin

from .models import MatVolumes, MatCategories, MatGroups, Materials, MaterialAds

# Register your models here.
# admin.site.register(MatVolumes)
# admin.site.register(MatCategories)
# admin.site.register(MatGroups)
# admin.site.register(Materials)


from import_export.admin import ImportExportModelAdmin
# Register MaterialAds Admin
class MaterialAdsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id', 'material_name', 'material_description', 'material_owner', 'material_region', 'company_stir']
    list_filter = ['material_name', 'material_description', 'material_owner', 'material_region', 'company_stir']
    # search_fields = ['material_name', 'material_description']

admin.site.register(MaterialAds, MaterialAdsAdmin)


# Register MatVolumes Admin
class MatVolumesAdmin(admin.ModelAdmin):
    list_display = ['id', 'volume_name', 'volume_desc', 'volume_logo']
    # list_filter = ['volume_name']
    ordering = ('id',)
    # search_fields = ['material_name', 'material_description']

admin.site.register(MatVolumes, MatVolumesAdmin)


# Register MatCategories Admin
class MatCategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'category_desc', 'category_volume']
    list_filter = ['category_volume']
    ordering = ('id', 'category_volume')
    # search_fields = ['material_name', 'material_description']

admin.site.register(MatCategories, MatCategoriesAdmin)


# Register MatCategories Admin
class MatGroupsAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name', 'group_desc', 'group_category']
    list_filter = ['group_category']
    ordering = ('id', 'group_category')
    search_fields = ['group_name', 'group_category']

admin.site.register(MatGroups, MatGroupsAdmin)


# Register MatCategories Admin
class MaterialsAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ['material_csr_code', 'material_name', 'material_measure', 'material_image', 'material_group']
    list_filter = ['material_measure', 'material_group']
    ordering = ('material_group', 'material_name')
    search_fields = ['material_name', 'material_csr_code']

admin.site.register(Materials, MaterialsAdmin)
