from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import ( 
CustomLanguages, SelectedThings, ResourcesList4Search, 
TexnikJTSA,Bojxona, BojxonaCategory, Iqtisod_Moliya,
 Document_Category, Document, Material_Soliq_Price
)



from rest_framework import serializers




class Material_Soliq_PriceSerializer(ModelSerializer):
    class Meta:
        model = Material_Soliq_Price
        fields = '__all__'


# Serializer for Document_Category
class DocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Document_Category
        fields = '__all__'

# Serializer for Document
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'









class ConstructionDataSerializer(serializers.Serializer):
    inn = serializers.IntegerField()
    certificate_number = serializers.IntegerField()





class TexnikJTSASerializer(ModelSerializer):
    class Meta:
        model = TexnikJTSA
        fields =  "__all__"



class CustomLanguagesSerializer(ModelSerializer):
    class Meta:
        model = CustomLanguages
        fields = '__all__'


class SelectedThingsSerializer(ModelSerializer):
    class Meta:
        model = SelectedThings
        fields = ('user', 'thing_id', 'thing_type')


# class SelectedThingsDeselectSerializer(ModelSerializer):
#     class Meta:
#         model = SelectedThings
#         fields = ('deselected',)


class SelectedThingsALLSerializer(ModelSerializer):
    class Meta:
        model = SelectedThings
        fields = '__all__'


class SearchedResourcesSerializer(ModelSerializer):
    resource_image = SerializerMethodField()

    class Meta:
        model = ResourcesList4Search
        fields = '__all__'

    def get_resource_image(self, obj):
        if not obj.resource_image:
            return None
        else:
            return f"https://backend-market.tmsiti.uz/media/{obj.resource_image}"



class BojxonaSerializer(ModelSerializer):
    class Meta:
        model = Bojxona
        fields = '__all__'


class BojxonaCategorySerializer(ModelSerializer):
    bojxona_set = BojxonaSerializer(many=True, write_only=True)

    class Meta:
        model = BojxonaCategory
        fields = ['bj_id', 'error', 'bojxona_set']

    def create(self, validated_data):
        tovars_data = validated_data.pop('bojxona_set')
        category = BojxonaCategory.objects.create(**validated_data)
        for tovar_data in tovars_data:
            Bojxona.objects.create(bj_category=category, **tovar_data)
        return category


class Iqtisod_Moliya_Serializer(ModelSerializer):
    class Meta:
        model =  Iqtisod_Moliya
        fields = "__all__"
