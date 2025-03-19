from django.contrib import admin

from .models import SmallMechanoCategories, SmallMechanoGroups, SmallMechano, SmallMechanoAds

# Register your models here.
# admin.site.register(SmallMechanoCategories)
# admin.site.register(SmallMechanoGroups)
# admin.site.register(SmallMechano)
# admin.site.register(SmallMechanoAds)



# Register SmallMechanoAds Admin
class SmallMechanoAdsAdmin(admin.ModelAdmin):
    list_display = ['id', 'smallmechano_name', 'smallmechano_description', 'smallmechano_owner', 'company_stir']
    list_filter = ['smallmechano_name', 'smallmechano_description', 'smallmechano_owner', 'company_stir']
    # search_fields = ['smallmechano_name', 'smallmechano_description']

admin.site.register(SmallMechanoAds, SmallMechanoAdsAdmin)


# Register SmallMechanoCategories Admin
class SmallMechanoCategoriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'category_name', 'category_desc', 'category_logo']
    ordering = ('id',)
    # search_fields = ['smallmechano_name', 'smallmechano_description']

admin.site.register(SmallMechanoCategories, SmallMechanoCategoriesAdmin)


# Register SmallMechanoCategories Admin
class SmallMechanoGroupsAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name', 'group_desc', 'group_category']
    list_filter = ['group_category']
    ordering = ('id', 'group_category')
    # search_fields = ['smallmechano_name', 'smallmechano_description']

admin.site.register(SmallMechanoGroups, SmallMechanoGroupsAdmin)


# Register SmallMechanoCategories Admin
class SmallMechanoAdmin(admin.ModelAdmin):
    list_display = ['smallmechano_csr_code', 'smallmechano_name', 'smallmechano_measure', 'smallmechano_image', 'smallmechano_group']
    list_filter = ['smallmechano_measure', 'smallmechano_group']
    ordering = ('smallmechano_group', 'smallmechano_name')
    search_fields = ['smallmechano_name', 'smallmechano_csr_code']

admin.site.register(SmallMechano, SmallMechanoAdmin)