from django.contrib.auth import get_user_model

from rest_framework.serializers import ModelSerializer, SerializerMethodField

from app_company.models import Companies

from .models import MatVolumes, MatCategories, MatGroups, Materials, MaterialsAllInfo, MaterialAds




class MaterialsAllInfoSerializer1(ModelSerializer):
    class Meta:
        model = MaterialAds
        fields = '__all__'


class MaterialCompanySerializer(ModelSerializer):
    class Meta:
        model = MaterialAds
        fields = ['company_name', 'company_stir']
        read_only_fields = ['company_name', 'company_stir']



class MatVolumesSerializer(ModelSerializer):
    volume_logo = SerializerMethodField()

    class Meta:
        model = MatVolumes
        fields = '__all__'

    def get_volume_logo(self, obj):
        return f"https://backend-market.tmsiti.uz/media/{obj.volume_logo}"

class MatCategoriesSerializer(ModelSerializer):
    class Meta:
        model = MatCategories
        fields = '__all__'

class MatGroupsSerializer(ModelSerializer):
    class Meta:
        model = MatGroups
        fields = '__all__'

class MaterialsSerializer(ModelSerializer):
    class Meta:
        model = Materials
        fields = '__all__'
        # fields = ['material_name', 'material_csr_code']

class MaterialsAllInfoSerializer(ModelSerializer):
    class Meta:
        model = MaterialsAllInfo
        fields = '__all__'

class MaterialAdsSerializer(ModelSerializer):
    phone_number = SerializerMethodField()
    material_code = SerializerMethodField()
    material_name = SerializerMethodField()
    material_image = SerializerMethodField()
    material_region  =  SerializerMethodField()	
    class Meta:
        model = MaterialAds
        fields = ['id', 'material_code', 'material_name', 'material_description', 'material_price', 'material_price_currency', 'material_measure', 'material_image', 'material_amount', 'material_amount_measure', 'material_created_date',  'material_updated_date', 'sertificate_blank_num', 'sertificate_reestr_num', 'material_owner', 'company_name', 'company_stir', 'phone_number', 'material_region', 'material_district']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_phone_number(self, obj):
        company = Companies.objects.filter(company_stir=obj.company_stir).first()
        if company:
            return company.company_phone_main
        return None  

    def get_material_region(self, obj):
        return obj.material_region.region_name_uz if obj.material_region else None
	

    def get_material_name(self, obj):
        try:
            return Materials.objects.filter(material_csr_code=obj.material_name_id)[0].material_name
        except:
            return obj.material_name_id

    def get_material_code(self, obj):
        return obj.material_name_id

    def get_material_image(self, obj):
        return f"https://backend-market.tmsiti.uz/media{obj.material_image}"

class MaterialAdsDeactivateSerializer(ModelSerializer):
    class Meta:
        model = MaterialAds
        fields = ['id', 'material_name', 'material_status']


import requests
class MaterialAdsManageSerializer(ModelSerializer):
    class Meta:
        model = MaterialAds
        fields = ['id', 'material_name', 'material_description', 'material_price', 'material_price_currency', 'material_measure', 'material_image', 'material_amount', 'material_amount_measure', 'material_created_date',  'material_updated_date', 'sertificate_blank_num', 'sertificate_reestr_num', 'company_name', 'company_stir', 'material_owner']
        extra_kwargs = {
            'id': {'read_only': True}
        }
    
    def create(self, validated_data):
        # instance = self.Meta.model(**validated_data)
        # instance.material_owner_id = self.user.id
        return MaterialAds.objects.create(**validated_data)
    def get_material_name(self, obj):
        material_name = obj.material_name
        if material_name:
            return material_name.material_name 
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Include material_name details
        data['material_csr_code'] = self.get_material_name(instance)

        return data



from rest_framework import serializers

class CompanyStirSerializer(serializers.Serializer):
    company_stir = serializers.CharField()
    company_name = serializers.CharField() 

class MaterialAdsSerializer1(serializers.ModelSerializer):
    class Meta:
        model = MaterialAds
        fields = '__all__'
