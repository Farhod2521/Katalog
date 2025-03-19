# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView

from rest_framework import  status
import jwt, datetime
from users.models import CatalogUsers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from django.views import View
from app_company.models import Companies

from config.pagination import CustomPagination

from .filters import MaterialSearchFilterBackend

from .models import MatVolumes, MatCategories, MatGroups, Materials, MaterialsAllInfo, MaterialAds
from .serializers import (
    MatVolumesSerializer, MatCategoriesSerializer, MatGroupsSerializer, MaterialsSerializer, MaterialsAllInfoSerializer,
    MaterialAdsSerializer, MaterialAdsDeactivateSerializer, MaterialAdsManageSerializer, MaterialAdsSerializer1, MaterialsAllInfoSerializer1, CompanyStirSerializer,MaterialCompanySerializer
    )



from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import  timedelta

 # 1Create your views here.
from rest_framework.pagination import PageNumberPagination


class MaterialAdsList(ListAPIView):
    serializer_class = MaterialAdsSerializer

    def get_queryset(self):
        start_date = timezone.make_aware(datetime.datetime(2024, 5, 1))
        end_date = timezone.make_aware(datetime.datetime.now() + timedelta(days=1))
        
        queryset = MaterialAds.objects.filter(
            material_created_date__range=(start_date, end_date)
        ).select_related(
            'material_name', 'material_owner', 'material_region', 'material_district'
        ).order_by('-material_updated_date')
        
        return queryset







from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import Lower
from django.db.models import Count
class MaterialRegionCompanyStir(APIView):
    serializer_class = CompanyStirSerializer

    def get(self, request, region, format=None):
        material_region = MaterialAds.objects.filter(material_region__region_name_uz=region)
        company_data = material_region.annotate(lower_company_name=Lower('company_name')).values('company_stir', 'company_name').annotate(count=Count('company_stir')).filter(count=1)
        serializer = self.serializer_class(company_data, many=True)
        return Response(serializer.data)








# APIs for working with MaterialsAllINFO
class MaterialsInfoDetailView(RetrieveAPIView):
    queryset = Materials.objects.all()
    serializer_class = MaterialsSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # API endpoint
        url = "https://tasnif.soliq.uz/api/cl-api/integration-kcm/kcm"

        # Request payload as a list
        payload = [instance.material_csr_code]  # Note the list format here

        try:
            # API request
            response = requests.post(url, json=payload)
            response_data = response.json()

            # Check for success and extract `mxikCode` value
            mxik_soliq_data = None
            if response_data.get("success") and response_data.get("data"):
                mxik_soliq_data = response_data["data"][0].get(instance.material_csr_code, {}).get("mxikCode")

            # Serialize the instance
            serializer = self.get_serializer(instance)
            response_data = serializer.data

            # Add `mxik_soliq` to the response data
            response_data["mxik_soliq"] = mxik_soliq_data

            return Response(response_data, status=status.HTTP_200_OK)

        except requests.RequestException as e:
            # Handle request error
            return Response(
                {"error": "Failed to fetch mxik_soliq data", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



# APIs for working with MaterialAds
class MaterialsAdsFilterByNameAPIListView(ListAPIView):
    serializer_class = MaterialAdsSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        keyword = self.kwargs['csr_code']
        if 'sort_by' in self.request.GET:
            col_name = self.request.GET['sort_by']
        else:
            col_name = 'material_updated_date'
        queryset = MaterialAds.objects.filter(material_status=True, material_name=keyword).order_by(col_name)
        
        if 'region' in self.request.GET:
            queryset = queryset.filter(material_region=self.request.GET['region'])
        
        if 'district' in self.request.GET:
            queryset = queryset.filter(material_district=self.request.GET['district'])
        return queryset




class MaterialsAdsFilterByUserAPIListView(ListAPIView):
    serializer_class = MaterialAdsSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        token = self.request.META.get('HTTP_TOKEN')

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_stir = payload['company_stir']
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')

        # Check for sorting criteria
        col_name = self.request.GET.get('sort_by', '-material_updated_date')

        # Ensure the queryset is ordered
        queryset = MaterialAds.objects.filter(material_status=True, company_stir=user_stir).order_by(col_name)

        # Return the ordered queryset
        return queryset



class MaterialsUniversalEndpointListView(ListAPIView):
    serializer_class = MaterialsAllInfoSerializer
    pagination_class = CustomPagination
    filter_backends = (MaterialSearchFilterBackend,)
    # queryset = MaterialsAllInfo.objects.all().order_by('material_views_count')
    def get_queryset(self):
        col_name = self.request.GET['key']
        
        if 'sort_by' in self.request.GET:
            col_order = self.request.GET['sort_by']
        else:
            col_order = 'material_name'
        
        if col_name == 'views_count':
            #queryset = MaterialAds.objects.all()
            queryset = MaterialsAllInfo.objects.all().order_by('-material_views_count')
        elif col_name == 'volume':
            col_value = self.request.GET['value']
            queryset = MaterialsAllInfo.objects.filter(material_volume=col_value).order_by(col_order)
        elif col_name == 'category':
            col_value = self.request.GET['value']
            queryset = MaterialsAllInfo.objects.filter(material_category=col_value).order_by(col_order)
        elif col_name == 'group':
            col_value = self.request.GET['value']
            queryset = MaterialsAllInfo.objects.filter(material_group=col_value).order_by(col_order)
        elif col_name == 'name':
            col_value = self.request.GET['value']
            queryset = MaterialsAllInfo.objects.filter(material_name__icontains=col_value).order_by(col_order)
        else:
            queryset = MaterialsAllInfo.objects.none()
        return queryset
        

# class MaterialAdsViewSet(ModelViewSet):
#     http_method_names = ['post', 'put', 'patch']
#     permission_classes = (permissions.IsAuthenticated,)
#     queryset = MaterialAds.objects.filter(material_status=True).order_by('id')
#     serializer_class = MaterialAdsSerializer


class MaterialAdsManageView(APIView):
    def post(self, request):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        # request.data['material_owner'] = payload['id']
        request.data['company_stir'] = payload['company_stir']
        request.data['company_name'] = payload['company_name']
        
        serializer = MaterialAdsManageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)




import requests
# UPdate qilish 
class MaterialAdsUpdateView(RetrieveUpdateAPIView):
    serializer_class = MaterialAdsManageSerializer
    queryset = MaterialAds.objects.all()
    http_method_names = ['get', 'put']  

    def retrieve(self, request, pk=None):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
           payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        # url1 = f"https://mspd-api.soliq.uz/minstroy/construction/get-factura-list-by-tin?fromDate=01.01.2024&tin=309219534&toDate=29.01.2024"
        # url1 = f"https://mspd-api.soliq.uz/minstroy/construction/get-factura-list-by-catalog-code?catalogCode=00407001001000000&fromDate=01.01.2024&toDate=10.01.2024"
        # response1 = requests.get(url1)

        # if response1.status_code == 200:
        #     data1 = response1.json()
        #     return Response(data1)
        # else:
        #     error_message = "Serverdan yaroqsiz javob qaytardi"
        #     return Response({'error': error_message}, status=response1.status_code)


        try:
            material_ads = self.get_queryset().get(id=pk)

            
            
            serializer = self.get_serializer(material_ads)
            
            return Response(serializer.data)
        except MaterialAds.DoesNotExist:
            return Response(data={'result': 'not found', 'description': 'MaterialAds not found'})
        except Exception as e:
            return Response(data={'result': 'error', 'description': str(e)})

    def update(self, request, *args, **kwargs):
    
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        instance = self.get_object()
        
        # Obyektni yangilash uchun serializer'ni yaratamiz va request ma'lumotlarini o'zgartiramiz
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(material_updated_date=datetime.datetime.now())
        
        
        return Response(data="{'result': 'success', 'description': 'E‘lon muvaffaqiyatli ozgartirldi!'}")






class MaterialAdsDeactivateView(UpdateAPIView):
    def update(self, request):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        # user_id = payload['id']
        user_stir = payload['company_stir']
        post_id = request.data['id']
        
        try:
            MaterialAds.objects.filter(id=post_id, company_stir=user_stir).update(material_status=False, material_deactivated_date=datetime.datetime.now())
            return Response(data="{'result': 'success', 'description': 'E‘lon muvaffaqiyatli o‘chirildi!'}")
        except Exception as e:
            return Response(data="{'result': 'error', 'description': str(e)}")





class MaterialAdsViewSet11(APIView):
    def get(self, request):
        queryset = MaterialAds.objects.values('company_name', 'company_stir').distinct()
        company_data = {}
        for item in queryset:
            company_stir = item['company_stir']
            if company_stir not in company_data:
                company_data[company_stir] = {
                    'company_name': item['company_name'],
                    'count': 1
                }
            else:
                company_data[company_stir]['count'] += 1
        
        serialized_data = []
        for company_stir, data in company_data.items():
            serialized_data.append({
                'company_name': data['company_name'],
                'count': data['count']
            })

        return Response(serialized_data, status=status.HTTP_200_OK)



class ExcelExportView(APIView):
    def get(self, request, *args, **kwargs):
        material_ads = MaterialAds.objects.all()
        serializer = MaterialAdsSerializer(material_ads, many=True)
        return Response(serializer.data)
