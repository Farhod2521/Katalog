from rest_framework.serializers import ModelSerializer

from .models import CSRVolumes, CSRParts, CSRChapters, CSRGroups, CSRResources, CSRResourcesAllInfos

class CSRVolumesSerializer(ModelSerializer):
    class Meta:
        model = CSRVolumes
        fields = '__all__'

class CSRPartsSerializer(ModelSerializer):
    class Meta:
        model = CSRParts
        fields = '__all__'

class CSRChaptersSerializer(ModelSerializer):
    class Meta:
        model = CSRChapters
        fields = '__all__'

class CSRGroupsSerializer(ModelSerializer):
    class Meta:
        model = CSRGroups
        fields = '__all__'

class CSRResourcesSerializer(ModelSerializer):
    class Meta:
        model = CSRResources
        fields = '__all__'

class CSRAllInfoSerializer(ModelSerializer):
    class Meta:
        model = CSRResourcesAllInfos
        fields = '__all__'