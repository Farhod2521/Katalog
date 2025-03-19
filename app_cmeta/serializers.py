from rest_framework import serializers
from .models import Cmeta, CmetaCategory, Sample_ProjectCategory, Sample_Project


class CmetaSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Cmeta
        fields= "__all__"


class CmetaCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  CmetaCategory
        fields= "__all__"



class Sample_ProjectCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model =  Sample_ProjectCategory
        fields= "__all__"

class Sample_ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model =  Sample_Project
        fields= "__all__"
