from rest_framework.serializers import ModelSerializer, SerializerMethodField

from app_company.models import Companies

from .models import WorkCategories, WorkGroups, Work, WorkAllInfo, WorkAds

class WorkCategoriesSerializer(ModelSerializer):
    category_logo = SerializerMethodField()

    class Meta:
        model = WorkCategories
        fields = '__all__'

    def get_category_logo(self, obj):
        return f"https://backend-market.tmsiti.uz/media/{obj.category_logo}"

class WorkGroupsSerializer(ModelSerializer):
    class Meta:
        model = WorkGroups
        fields = '__all__'

class WorkSerializer(ModelSerializer):
    class Meta:
        model = Work
        fields = ['work_name', 'work_csr_code']

class WorkAllInfoSerializer(ModelSerializer):
    work_image = SerializerMethodField()

    class Meta:
        model = WorkAllInfo
        fields = '__all__'

    def get_work_image(self, obj):
        return f"https://backend-market.tmsiti.uz/media/{obj.work_image}"



class WorkAdsDeactivateSerializer(ModelSerializer):
    class Meta:
        model = WorkAds
        fields = ['id', 'work_name', 'work_status']



class WorkAdsManageSerializer(ModelSerializer):
    class Meta:
        model =  WorkAds
        fields = ['id', 'work_name', 'work_description', 'work_rent_price', 'work_image', 
                  'work_created_date', 'work_rent_price_currency', 'work_measure',
                    'work_amount', 'work_amount_measure', 'sertificate_reestr_num', 'sertificate_blank_num', 
                   'work_owner', 'company_name', 'company_stir', ]
        extra_kwargs = {
            'id': {'read_only': True}
        }
    
    def create(self, validated_data):
        # instance = self.Meta.model(**validated_data)
        # instance.Techno_owner_id = self.user.id
        return WorkAds.objects.create(**validated_data)
    
    def get_work_name(self, obj):
        work_name = obj.work_name
        if work_name:
            return work_name.work_name 
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        
        # Include work_name details
        data['material_csr_code'] = self.get_work_name(instance)

        return data    


class WorkAdsSerializer(ModelSerializer):
    phone_number = SerializerMethodField()
    work_code =  SerializerMethodField()
    work_name = SerializerMethodField()
    work_image = SerializerMethodField()
    class Meta:
        model =  WorkAds
        fields = ['id', 'work_code','work_image', 'work_name', 'work_description', 'work_rent_price', 'work_image', 
                  'work_created_date', 'work_rent_price_currency', 'work_measure',
                    'work_amount', 'work_amount_measure', 'sertificate_reestr_num', 'sertificate_blank_num', 
                   'work_owner', 'company_name', 'company_stir','phone_number' ]
        extra_kwargs = {
            'id': {'read_only': True}
        }

    def get_work_name(self, obj):
        try:
            return WorkAds.objects.filter(techno_csr_code=obj.work_name_id)[0].work_name
        except:
            return obj.work_name_id

    def get_work_code(self, obj):
        return obj.work_name_id
    
    def get_phone_number(self, obj):
        return Companies.objects.filter(company_stir=obj.company_stir)[0].company_phone_main
    def get_work_image(self, obj):
        return f"https://backend-market.tmsiti.uz/media/{obj.work_image}"
