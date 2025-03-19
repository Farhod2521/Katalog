from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView
from .models import Cmeta, CmetaCategory,  Sample_ProjectCategory, Sample_Project
from .serializers import CmetaSerializer, CmetaCategorySerializer, Sample_ProjectCategorySerializer,  Sample_ProjectSerializer
from rest_framework.response import Response
class CmetaApiView(ListAPIView):
    serializer_class =  CmetaSerializer
    permission_classes =  [AllowAny]

    def get_queryset(self):
        category_id  =  self.kwargs.get('category_id')
        if category_id:
            return Cmeta.objects.filter(category_id=category_id)
        return Response(data={
            "status":False,
            "message":"catagory ID mavjud emas"
        })

class CmetaCategoryApiView(ListAPIView):
    queryset = CmetaCategory.objects.all()
    serializer_class = CmetaCategorySerializer
    permission_classes = [AllowAny]
# Create your views here.



class Sample_ProjectApiView(ListAPIView):
    serializer_class =  Sample_ProjectSerializer
    permission_classes =  [AllowAny]

    def get_queryset(self):
        category_id  =  self.kwargs.get('category_id')
        if category_id:
            return Sample_Project.objects.filter(category_id=category_id).order_by("-id")
        return Response(data={
            "status":False,
            "message":"catagory ID mavjud emas"
        })

class Sample_ProjectCategoryApiView(ListAPIView):
    queryset = Sample_ProjectCategory.objects.all()
    serializer_class = Sample_ProjectCategorySerializer
    permission_classes = [AllowAny]
