from rest_framework.serializers import ModelSerializer, SerializerMethodField

from app_company.models import Companies

from .models import TechnoVolumes, TechnoCategories, TechnoGroups, Techno, TechnoAllInfo, TechnoAds

class TechnoVolumesSerializer(ModelSerializer):
    volume_logo = SerializerMethodField()

    class Meta:
        model = TechnoVolumes
        fields = '__all__'

    def get_volume_logo(self, obj):
        return f"https://backend-market.tmsiti.uz/media/{obj.volume_logo}"

class TechnoCategoriesSerializer(ModelSerializer):
    class Meta:
        model = TechnoCategories
        fields = '__all__'

class TechnoGroupsSerializer(ModelSerializer):
    class Meta:
        model = TechnoGroups
        fields = '__all__'

class TechnoSerializer(ModelSerializer):
    class Meta:
        model = Techno
        fields = ['techno_name', 'techno_csr_code']

class TechnoAllInfoSerializer(ModelSerializer):
    class Meta:
        model = TechnoAllInfo
        fields = '__all__'

class TechnoAdsSerializer(ModelSerializer):
    phone_number = SerializerMethodField()
    techno_code = SerializerMethodField()
    techno_name = SerializerMethodField()
    
    class Meta:
        model = TechnoAds
        fields = ['id', 'techno_code', 'techno_name', 'techno_description', 'techno_price', 'techno_price_currency', 'techno_measure', 'techno_image', 'techno_amount', 'techno_amount_measure', 'techno_created_date', 'sertificate_blank_num', 'sertificate_reestr_num', 'techno_owner', 'company_name', 'company_stir', 'phone_number']
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_techno_name(self, obj):
        try:
            return Techno.objects.filter(techno_csr_code=obj.techno_name_id)[0].techno_name
        except:
            return obj.techno_name_id

    def get_techno_code(self, obj):
        return obj.techno_name_id
    
    def get_phone_number(self, obj):
        return Companies.objects.filter(company_stir=obj.company_stir)[0].company_phone_main

class TechnoAdsDeactivateSerializer(ModelSerializer):
    class Meta:
        model = TechnoAds
        fields = ['id', 'techno_name', 'techno_status']



class TechnoAdsManageSerializer(ModelSerializer):
    class Meta:
        model = TechnoAds
        fields = ['id', 'techno_name', 'techno_description', 'techno_price', 'techno_price_currency', 'techno_measure', 'techno_image', 'techno_amount', 'techno_amount_measure', 'techno_created_date', 'sertificate_blank_num', 'sertificate_reestr_num', 'techno_owner', 'company_name', 'company_stir']
        extra_kwargs = {
            'id': {'read_only': True}
        }
    
    def create(self, validated_data):
        # instance = self.Meta.model(**validated_data)
        # instance.Techno_owner_id = self.user.id
        return TechnoAds.objects.create(**validated_data)
