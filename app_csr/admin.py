from django.contrib import admin
from .models import CSRVolumes, CSRParts, CSRChapters, CSRGroups, CSRResources#, CSRResourcesAllInfos

# Register your models here.
# admin.site.register(CSRVolumes)
# admin.site.register(CSRParts)
# admin.site.register(CSRChapters)
# admin.site.register(CSRGroups)
# admin.site.register(CSRResources)
# admin.site.register(CSRResourcesAllInfos)


# Register Classifier Volumes Admin
class CSRVolumesAdmin(admin.ModelAdmin):
    list_display = ['id', 'volume_name', 'volume_code']
    # list_filter = ['volume_name']
    ordering = ('id',)
    # search_fields = ['material_name', 'material_description']

admin.site.register(CSRVolumes, CSRVolumesAdmin)


# Register Classifier Parts Admin
class CSRPartsAdmin(admin.ModelAdmin):
    list_display = ['id', 'part_name', 'part_code', 'part_volume']
    list_filter = ['part_volume']
    ordering = ('id', 'part_volume')
    search_fields = ['part_name']

admin.site.register(CSRParts, CSRPartsAdmin)


# Register Classifier Chapters Admin
class CSRChaptersAdmin(admin.ModelAdmin):
    list_display = ['id', 'chapter_name', 'chapter_code', 'chapter_part']
    list_filter = ['chapter_part']
    ordering = ('id', 'chapter_part')
    search_fields = ['chapter_name']

admin.site.register(CSRChapters, CSRChaptersAdmin)


# Register Classifier Chapters Admin
class CSRGroupsAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name', 'group_code', 'group_chapter']
    list_filter = ['group_chapter']
    ordering = ('id', 'group_chapter')
    search_fields = ['group_name']

admin.site.register(CSRGroups, CSRGroupsAdmin)


# Register Classifier Chapters Admin
class CSRResourcesAdmin(admin.ModelAdmin):
    list_display = ['id', 'resource_name', 'resource_code', 'resource_measure', 'resource_type', 'resource_group']
    list_filter = ['resource_measure', 'resource_type', 'resource_group']
    ordering = ('id', 'resource_group', 'resource_code')
    search_fields = ['resource_name']

admin.site.register(CSRResources, CSRResourcesAdmin)