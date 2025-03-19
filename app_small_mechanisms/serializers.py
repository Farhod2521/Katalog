from rest_framework.serializers import ModelSerializer, SerializerMethodField

from app_company.models import Companies

from .models import SmallMechanoCategories, SmallMechanoGroups, SmallMechano, SmallMechanoAllInfo, SmallMechanoAds

class SmallMechanoCategoriesSerializer(ModelSerializer):
    category_logo = SerializerMethodField()

    class Meta:
        model = SmallMechanoCategories
        fields = '__all__'

    def get_category_logo(self, obj):
        return f"https://backend-market.tmsiti.uz/media/{obj.category_logo}"

class SmallMechanoGroupsSerializer(ModelSerializer):
    class Meta:
        model = SmallMechanoGroups
        fields = '__all__'

class SmallMechanoSerializer(ModelSerializer):
    class Meta:
        model = SmallMechano
        fields = ['smallmechano_name', 'smallmechano_csr_code']

class SmallMechanoAllInfoSerializer(ModelSerializer):
    class Meta:
        model = SmallMechanoAllInfo
        fields = '__all__'


class SmallMechanoAdsDeactivateSerializer(ModelSerializer):
    class Meta:
        model = SmallMechanoAds
        fields = ['id', 'smallmechano_name', 'smallmechano_status']


class SmallMechanoAdsManageSerializer(ModelSerializer):
    class Meta:
        model = SmallMechanoAds
        fields = ['id', 'smallmechano_name', 'smallmechano_description', 'smallmechano_rent_price', 'smallmechano_rent_price_currency', 'smallmechano_measure', 'smallmechano_image', 'smallmechano_amount', 'smallmechano_amount_measure', 'smallmechano_created_date', 'smallmechano_updated_date', 'sertificate_blank_num', 'sertificate_reestr_num', 'smallmechano_owner', 'company_name', 'company_stir']
    
    def create(self, validated_data):
        # instance = self.Meta.model(**validated_data)
        # instance.Techno_owner_id = self.user.id
        return SmallMechanoAds.objects.create(**validated_data)
    
    def get_smallmechano_name(self, obj):
        smallmechano_name = obj.smallmechano_name
        if smallmechano_name:
            return smallmechano_name.smallmechano_name 
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Include smallmechano_name details
        data['material_csr_code'] = self.get_smallmechano_name(instance)

        return data



class SmallMechanoAdsSerializer(ModelSerializer):
    phone_number = SerializerMethodField()
    smallmechano_code = SerializerMethodField()
    smallmechano_name = SerializerMethodField()
    smallmechano_image = SerializerMethodField()
    
    class Meta:
        model = SmallMechanoAds
        fields = [
            'id', 'smallmechano_code',  'smallmechano_name', 
            'smallmechano_description', 'smallmechano_rent_price', 
            'smallmechano_rent_price_currency', 'smallmechano_measure', 
            'smallmechano_image', 'smallmechano_amount', 'smallmechano_amount_measure', 
            'smallmechano_created_date', 'smallmechano_updated_date', 
            'sertificate_blank_num', 'sertificate_reestr_num', 'smallmechano_owner', 
            'company_name', 'company_stir', 'phone_number'
        ]
        extra_kwargs = {
            'id': {'read_only': True}
        }
    

    
    def get_smallmechano_name(self, obj):
        try:
            return SmallMechano.objects.filter(smallmechano_csr_code=obj.smallmechano_name_id).first().smallmechano_name
        except SmallMechano.DoesNotExist:
            return obj.smallmechano_name_id
        
    def get_smallmechano_code(self, obj):
        return obj.smallmechano_name_id
    
    def get_phone_number(self, obj):
        return Companies.objects.filter(company_stir=obj.company_stir).first().company_phone_main
    

    
    def get_smallmechano_image(self, obj):
        return f"https://backend-market.tmsiti.uz/media{obj.smallmechano_image}"
