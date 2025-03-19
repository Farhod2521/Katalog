from django.contrib import admin

from .models import TechnoVolumes, TechnoCategories, TechnoGroups, Techno, TechnoAds

# Register your models here.
# admin.site.register(TechnoVolumes)
# admin.site.register(TechnoCategories)
# admin.site.register(TechnoGroups)
# admin.site.register(Techno)
# admin.site.register(TechnoAds)


from import_export.admin import ImportExportModelAdmin

# Register TechnoAds Admin
class TechnoAdsAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['id', 'techno_name', 'techno_description', 'techno_owner', 'company_stir', 'techno_region']
    list_filter = ['techno_name', 'techno_description', 'techno_owner', 'company_stir', 'techno_region']
    # search_fields = ['techno_name', 'techno_description']

admin.site.register(TechnoAds, TechnoAdsAdmin)

# Register TechnoVolumes Admin
class TechnoVolumesAdmin(admin.ModelAdmin):
    list_display = ['id', 'volume_name', 'volume_desc', 'volume_logo']
    # list_filter = ['volume_name']
    ordering = ('id',)
    # search_fields = ['techno_name', 'techno_description']

admin.site.register(TechnoVolumes, TechnoVolumesAdmin)


# Register TechnoCategories Admin
class TechnoCategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'category_desc', 'category_volume']
    list_filter = ['category_volume']
    ordering = ('id', 'category_volume')
    # search_fields = ['techno_name', 'techno_description']

admin.site.register(TechnoCategories, TechnoCategoriesAdmin)


# Register TechnoCategories Admin
class TechnoGroupsAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name', 'group_desc', 'group_category']
    list_filter = ['group_category']
    ordering = ('id', 'group_category')
    # search_fields = ['techno_name', 'techno_description']

admin.site.register(TechnoGroups, TechnoGroupsAdmin)


# Register TechnoCategories Admin
class TechnoAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['techno_csr_code', 'techno_name', 'techno_measure', 'techno_image', 'techno_group']
    list_filter = ['techno_measure', 'techno_group']
    ordering = ('techno_group', 'techno_name')
    search_fields = ['techno_name', 'techno_csr_code']

admin.site.register(Techno, TechnoAdmin)
