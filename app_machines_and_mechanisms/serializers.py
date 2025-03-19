from rest_framework.serializers import ModelSerializer, SerializerMethodField

from app_company.models import Companies

from .models import MMechanoCategories, MMechanoGroups, MMechano, MMechanoAllInfo, MMechanoAds, MMechnoAdExcel

class MMechanoCategoriesSerializer(ModelSerializer):
    category_logo = SerializerMethodField()

    class Meta:
        model = MMechanoCategories
        fields = '__all__'

    def get_category_logo(self, obj):
        return f"https://backend-market.tmsiti.uz/media/{obj.category_logo}";

class MMechanoGroupsSerializer(ModelSerializer):
    class Meta:
        model = MMechanoGroups
        fields = '__all__'

class MMechanoSerializer(ModelSerializer):
    class Meta:
        model = MMechano
        fields = ['mmechano_name', 'mmechano_csr_code']

class MMechanoAllInfoSerializer(ModelSerializer):
    class Meta:
        model = MMechanoAllInfo
        fields = '__all__'




class MMechanoAdsSerializer(ModelSerializer):
    phone_number = SerializerMethodField()
    mmechano_code = SerializerMethodField()
    mmechano_name = SerializerMethodField()
    mmechano_image = SerializerMethodField()
    
    class Meta:
        model = MMechanoAds
        fields = [
            'id', 'mmechano_code', 'mmechano_name', 'mmechano_description', 
            'mmechano_rent_price', 'mmechano_rent_price_currency', 'mmechano_measure', 
            'mmechano_image', 'mmechano_amount', 'mmechano_amount_measure', 
            'mmechano_created_date', 'mmechano_updated_date', 'sertificate_blank_num', 
            'sertificate_reestr_num', 'mmechano_owner', 'company_name', 'company_stir', 
            'phone_number'
        ]
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_mmechano_name(self, obj):
        try:
            return MMechano.objects.filter(mmechano_csr_code=obj.mmechano_name_id).first().mmechano_name
        except MMechano.DoesNotExist:
            return obj.mmechano_name_id
        
    def get_mmechano_code(self, obj):
        return obj.mmechano_name_id
    
    def get_phone_number(self, obj):
        return Companies.objects.filter(company_stir=obj.company_stir).first().company_phone_main
    
    def get_mmechano_image(self, obj):
        return f"https://backend-market.tmsiti.uz/media{obj.mmechano_image}"




class MMechanoAdsDeactivateSerializer(ModelSerializer):
    class Meta:
        model = MMechanoAds
        fields = ['id', 'mmechano_name', 'mmechano_status']




class MMechanoAdsManageSerializer(ModelSerializer):
    class Meta:
        model = MMechanoAds
        fields = ['id', 'mmechano_name', 'mmechano_description', 'mmechano_rent_price', 'mmechano_rent_price_currency', 'mmechano_measure', 'mmechano_image', 'mmechano_amount', 'mmechano_amount_measure', 'mmechano_created_date', 'mmechano_updated_date', 'sertificate_blank_num', 'sertificate_reestr_num', 'mmechano_owner', 'company_name', 'company_stir']
        extra_kwargs = {
            'id': {'read_only': True}
        }
    def create(self, validated_data):
        # instance = self.Meta.model(**validated_data)
        # instance.Techno_owner_id = self.user.id
        return MMechanoAds.objects.create(**validated_data)
    
    def get_mmechano_name(self, obj):
        mmechano_name = obj.mmechano_name
        if mmechano_name:
            return mmechano_name.mmechano_name 
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Include mmechano_name details
        data['material_csr_code'] = self.get_mmechano_name(instance)

        return data



class MMechnoAdExcelSerializer(ModelSerializer):
    class Meta:
        model = MMechnoAdExcel
        fields = "__all__"
        
