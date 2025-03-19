from rest_framework.serializers import ModelSerializer

from .models import ProductVolumes, ProductCategories, ProductGroups, Product, ProductAllInfo, ProductAds

class ProductVolumesSerializer(ModelSerializer):
    class Meta:
        model = ProductVolumes
        fields = '__all__'

class ProductCategoriesSerializer(ModelSerializer):
    class Meta:
        model = ProductCategories
        fields = '__all__'

class ProductGroupsSerializer(ModelSerializer):
    class Meta:
        model = ProductGroups
        fields = '__all__'

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_csr_code']

class ProductAllInfoSerializer(ModelSerializer):
    class Meta:
        model = ProductAllInfo
        fields = '__all__'

class ProductAdsSerializer(ModelSerializer):
    class Meta:
        model = ProductAds
        fields = ['id', 'product_name', 'product_description', 'product_price', 'product_price_currency', 'product_measure', 'product_image', 'product_amount', 'product_amount_measure', 'product_created_date', 'sertificate_blank_num', 'sertificate_reestr_num', 'product_owner']

class ProductAdsDeactivateSerializer(ModelSerializer):
    class Meta:
        model = ProductAds
        fields = ['id', 'product_name', 'product_status']