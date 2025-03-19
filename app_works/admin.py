from django.contrib import admin

from .models import WorkCategories, WorkGroups, Work, WorkAds

# Register your models here.
# admin.site.register(WorkCategories)
# admin.site.register(WorkGroups)
# admin.site.register(Work)
# admin.site.register(WorkAds)



# Register MaterialAds Admin
class WorkAdsAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_name', 'work_description', 'work_owner', 'company_stir']
    list_filter = ['work_name', 'work_description', 'work_owner', 'company_stir']
    # search_fields = ['work_name', 'work_description']

admin.site.register(WorkAds, WorkAdsAdmin)


# Register WorkCategories Admin
class WorkCategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'category_desc', 'category_logo']
    ordering = ('id',)
    # search_fields = ['work_name', 'work_description']

admin.site.register(WorkCategories, WorkCategoriesAdmin)


# Register WorkCategories Admin
class WorkGroupsAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name', 'group_desc', 'group_category']
    list_filter = ['group_category']
    ordering = ('id', 'group_category')
    # search_fields = ['work_name', 'work_description']

admin.site.register(WorkGroups, WorkGroupsAdmin)


# Register WorkCategories Admin
class WorkAdmin(admin.ModelAdmin):
    list_display = ['work_csr_code', 'work_name', 'work_measure', 'work_image', 'work_group']
    list_filter = ['work_measure', 'work_group']
    ordering = ('work_group', 'work_name')
    search_fields = ['work_name', 'work_csr_code']

admin.site.register(Work, WorkAdmin)