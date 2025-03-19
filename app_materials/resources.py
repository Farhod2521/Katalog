from import_export import resources

from .models import MatVolumes, MatCategories, MatGroups, Materials, MaterialsAllInfo, MaterialAds


from import_export.formats.base_formats import XLSX

class MaterialAdsResource(resources.ModelResource):
    def export(self, queryset=None, *args, **kwargs):
        if queryset is None:
            queryset = self.get_queryset()
        dataset = self.export_data(queryset, *args, **kwargs)
        # Write dataset to file in chunks or handle export logic here
        return dataset
