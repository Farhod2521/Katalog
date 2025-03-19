from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Regions, Districts, Companies, AllAds
from app_materials.models import  MaterialAds

class UzbRegionsSerializer(ModelSerializer):
    class Meta:
        model = Regions
        fields = ('id', 'region_name')


class UzbDistrictsSerializer(ModelSerializer):
    class Meta:
        model = Districts
        fields = ('id', 'district_name', 'district_type', 'district_region_id')


class CompaniesSerializer(ModelSerializer):
    class Meta:
        model = Companies
        fields = '__all__'

class CompaniesUpdateSerializer(ModelSerializer):
    class Meta:
        model = Companies
        fields = ['company_email',"company_phone_main", "company_phone_other","company_ceo", "company_address"  ]


class CompanyAllAdsSerializer(ModelSerializer):
    material_image = SerializerMethodField()
    material_name = SerializerMethodField()
    material_csr_code = SerializerMethodField()
    material_region = SerializerMethodField()

    class Meta:
        model = MaterialAds
        fields = [
            "id", "material_name", "material_csr_code", "material_image", "material_description",
            "material_price", "material_price_currency", "material_measure", "material_amount",
            "material_amount_measure", "material_status", "material_created_date", "material_updated_date",
            "material_deactivated_date", "sertificate_blank_num", "sertificate_reestr_num",
            "company_name", "company_stir", "material_owner", "material_region", "material_district"
        ]

    def get_material_image(self, obj):
        return f"https://backend-market.tmsiti.uz/media/{obj.material_image}"

    def get_material_name(self, obj):
        return obj.material_name.material_name

    def get_material_csr_code(self, obj):
        return obj.material_name.material_csr_code

    def get_material_region(self, obj):
        return obj.material_region.region_name_uz if obj.material_region else None
