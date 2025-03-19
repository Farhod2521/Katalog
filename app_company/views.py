from django.db.models import F

from .filters import NameFilterBackend, AllAdsFilterBackend

from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView,  RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


from .models import Regions, Districts, Companies, AllAds

from .serializers import UzbRegionsSerializer, UzbDistrictsSerializer,CompaniesUpdateSerializer , CompaniesSerializer, CompanyAllAdsSerializer

from config.pagination import LimitlessPagination, CustomPagination
from app_materials.models import   MaterialAds

from rest_framework.permissions import IsAuthenticated

from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime





from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class Company_Region_Filter(ListAPIView):
    serializer_class = CompaniesSerializer

    def get_queryset(self):
        region = self.kwargs.get('region')
        if region:
            return Companies.objects.filter(company_region__region_name_uz=region)
        else:
            return Companies.objects.none()  






class UzbTerritoriesListView(ListAPIView):
    pagination_class = LimitlessPagination
    
    def get_serializer_class(self):
        if 'key' in self.request.GET:
            table_name = self.request.GET['key']
        else:
            table_name = 'regions'
        
        if table_name == 'regions':
            serializer_class = UzbRegionsSerializer
        elif table_name == 'districts':
            serializer_class = UzbDistrictsSerializer
        else:
            serializer_class = UzbRegionsSerializer
        
        return serializer_class
    
    def get_queryset(self):
        if 'key' in self.request.GET:
            table_name = self.request.GET['key']
        else:
            table_name = 'regions'
        
        if 'lang' in self.request.GET:
            lang = self.request.GET['lang']
        else:
            lang = 'uz'
        
        
        if table_name == 'regions':
            if lang == 'uz':
                queryset = Regions.objects.all().values('id', 'region_name_uz').annotate(region_name=F('region_name_uz'))
            elif lang == 'en':
                queryset = Regions.objects.all().values('id', 'region_name_en').annotate(region_name=F('region_name_en'))
            elif lang == 'ru':
                queryset = Regions.objects.all().values('id', 'region_name_ru').annotate(region_name=F('region_name_ru'))
            else:
                queryset = Regions.objects.all().values('id', 'region_name_uz').annotate(region_name=F('region_name_uz'))
            return queryset
        
        elif table_name == 'districts':
            if 'filter' in self.request.GET:
                fk = self.request.GET['filter']
                if lang == 'uz':
                    queryset = Districts.objects.filter(district_region=fk).values('id', 'district_name_uz', 'district_type', 'district_region_id').annotate(district_name=F('district_name_uz'))
                elif lang == 'en':
                    queryset = Districts.objects.filter(district_region=fk).values('id', 'district_name_en', 'district_type', 'district_region_id').annotate(district_name=F('district_name_en'))
                elif lang == 'ru':
                    queryset = Districts.objects.filter(district_region=fk).values('id', 'district_name_ru', 'district_type', 'district_region_id').annotate(district_name=F('district_name_ru'))
                else:
                    queryset = Districts.objects.filter(district_region=fk).values('id', 'district_name_uz', 'district_type', 'district_region_id').annotate(district_name=F('district_name_uz'))
                return queryset
            else:
                if lang == 'uz':
                    queryset = Districts.objects.all().values('id', 'district_name_uz', 'district_type', 'district_region_id').annotate(district_name=F('district_name_uz'))
                elif lang == 'en':
                    queryset = Districts.objects.all().values('id', 'district_name_en', 'district_type', 'district_region_id').annotate(district_name=F('district_name_en'))
                elif lang == 'ru':
                    queryset = Districts.objects.all().values('id', 'district_name_ru', 'district_type', 'district_region_id').annotate(district_name=F('district_name_ru'))
                else:
                    queryset = Districts.objects.all().values('id', 'district_name_uz', 'district_type', 'district_region_id').annotate(district_name=F('district_name_uz'))
                return queryset


class CompaniesListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = CompaniesSerializer
    queryset = Companies.objects.all()
    filter_backends = (NameFilterBackend,)
    pagination_class = CustomPagination


class CompanyDetailView(RetrieveAPIView):
    serializer_class = CompaniesSerializer
    queryset = Companies.objects.all()


class CompanyAdsAPIListView(ListAPIView):
    serializer_class = CompanyAllAdsSerializer
    pagination_class = CustomPagination
    filter_backends = (AllAdsFilterBackend, )

    def get_queryset(self):
        keyword = self.kwargs['stir']
        col_name = self.request.GET.get('sort_by', 'material_updated_date')

        queryset = MaterialAds.objects.filter(company_stir=keyword).select_related(
            "material_name",  # ForeignKey to Materials
            "material_region"  # ForeignKey to Regions
        ).order_by(col_name)

        if 'region' in self.request.GET:
            queryset = queryset.filter(material_region=self.request.GET['region'])

        if 'district' in self.request.GET:
            queryset = queryset.filter(material_district=self.request.GET['district'])

        return queryset




class Company_Infarmation(APIView):
    # pagination_class = CustomPagination  # Pagination is not needed here since we are returning a single result
    serializer_class = CompaniesSerializer

    def get(self, request, *args, **kwargs):
        token = request.META['HTTP_TOKEN']
        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        company = Companies.objects.filter(company_stir=payload["company_stir"]).first()
        
        if company is not None:
            serializer = CompaniesSerializer(company)
            return Response([serializer.data])  # Wrap the serialized data in a list
        else:
            return Response({"detail": "No Companies matches the given query."}, status=status.HTTP_404_NOT_FOUND)
        





class Company_Info_UpdateView(APIView):
    serializer_class = CompaniesUpdateSerializer
    
    def post(self, request, *args, **kwargs):
        token = request.META.get("HTTP_TOKEN")

        if not token:
            raise AuthenticationFailed("Invalid token, login again, please")
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired login again please")
        
        instance = Companies.objects.get(company_stir=payload["company_stir"])

        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={
            "result": "success",
            "description": "Bajarildi"
        })
