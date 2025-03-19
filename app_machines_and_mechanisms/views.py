from rest_framework import permissions
# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, RetrieveUpdateAPIView


import jwt, datetime
from users.models import CatalogUsers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from app_company.models import Companies

from config.pagination import CustomPagination

from .models import MMechanoCategories, MMechanoGroups, MMechano, MMechanoAllInfo, MMechanoAds, MMechnoAdExcel
from .serializers import (
    MMechanoCategoriesSerializer, MMechanoGroupsSerializer, MMechanoSerializer, MMechanoAllInfoSerializer,
    MMechanoAdsSerializer, MMechanoAdsDeactivateSerializer, MMechanoAdsManageSerializer, MMechnoAdExcelSerializer
    )

# Create your views here.

# APIs for working with MMechano
class MMechanoInfoDetailView(RetrieveAPIView):
    queryset = MMechano.objects.all()
    serializer_class = MMechanoSerializer


# APIs for working with MMechanoAllINFO
class MMechanoAdsFilterByNameAPIListView(ListAPIView):
    serializer_class = MMechanoAdsSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        keyword = self.kwargs['csr_code']
        if 'sort_by' in self.request.GET:
            col_name = self.request.GET['sort_by']
        else:
            col_name = 'mmechano_updated_date'
        queryset = MMechanoAds.objects.filter(mmechano_status=True, mmechano_name=keyword, company_name__isnull=False).order_by(col_name)
        return queryset


class MMechanoUniversalEndpointListView(ListAPIView):
    serializer_class = MMechanoAllInfoSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        col_name = self.request.GET['key']
        
        if 'sort_by' in self.request.GET:
            col_order = self.request.GET['sort_by']
        else:
            col_order = 'mmechano_name'
        
        if col_name == 'views_count':
            queryset = MMechanoAllInfo.objects.all().order_by('-mmechano_views_count')
        elif col_name == 'category':
            col_value = self.request.GET['value']
            queryset = MMechanoAllInfo.objects.filter(mmechano_category=col_value).order_by(col_order)
        elif col_name == 'group':
            col_value = self.request.GET['value']
            queryset = MMechanoAllInfo.objects.filter(mmechano_group=col_value).order_by(col_order)
        elif col_name == 'name':
            col_value = self.request.GET['value']
            queryset = MMechanoAllInfo.objects.filter(mmechano_name__icontains=col_value).order_by(col_order)
        else:
            queryset = MMechanoAllInfo.objects.none()
        return queryset




class MMechanoAdsManageView(APIView):
    def post(self, request):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        #request.data['mmechano_owner'] = payload['id']
        request.data['company_stir'] = payload['company_stir']
        company = Companies.objects.filter(pk=payload['company_stir']).first()
        request.data['company_name'] = company.company_name
        
        serializer = MMechanoAdsManageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class MMechanoAdsDeactivateView(UpdateAPIView):
    def update(self, request):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        user_id = payload['id']
        post_id = request.data['id']
        
        try:
            MMechanoAds.objects.filter(id=post_id, mmechano_owner=user_id).update(mmechano_status=False, mmechano_deactivated_date=datetime.datetime.now())
            return Response(data="{'result': 'success', 'description': 'E‘lon muvaffaqiyatli o‘chirildi!'}")
        except Exception as e:
            return Response(data="{'result': 'error', 'description': str(e)}")




class MMechanoAdsFilterByUserAPIListView(ListAPIView):
    serializer_class = MMechanoAdsSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        token = self.request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_stir = payload['company_stir']
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        if 'sort_by' in self.request.GET:
            col_name = self.request.GET['sort_by']
        else:
            col_name = '-mmechano_updated_date'
        
        queryset = MMechanoAds.objects.filter(mmechano_status=True, company_stir=user_stir).order_by(col_name)
        
        return queryset



class MMechnoAdsUpdateView(RetrieveUpdateAPIView):
    serializer_class = MMechanoAdsManageSerializer
    queryset =  MMechanoAds.objects.all()
    http_method_names = ['get', 'put']


    def retrieve(self, request, pk=None):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
           payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        try:
            mmechno_ads = self.queryset.get(id=pk)
            serializer = self.get_serializer(mmechno_ads)
            return Response(serializer.data)
        except MMechanoAds.DoesNotExist:
            return Response(
                data={
                    "result":"not found",
                    "description": "MMechanoAds not found "
                }
            )
    
    def update(self, request, *args, **kwargs):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')

        instance  =  self.get_object()

        serializer =  self.get_serializer(instance, data=request.data, partial=True) 
        serializer.is_valid(raise_exception=True)
        serializer.save(mmechano_updated_date=datetime.datetime.now())
        return Response(
            data={
                "result": "Success",
                "des": "Baza muvfaqiyatli saqlandi!"
            }
        )
    
class MMechnoAdsDeleteView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        user_stir = payload['company_stir']
        post_id =  request.data['id']

        try:
            MMechanoAds.objects.get(id=post_id, company_stir=user_stir).delete()
            return Response(
                data={
                    "result":"succes",
                    "description":"E'lon o'chirildi "
                }
            )
        except Exception as e:
            return Response(
                data={
                    "result":"error",
                    "descriptions": "str(e)"
                }
            )


class MMechnoAdExcelListApiview(ListAPIView):
    serializer_class = MMechnoAdExcelSerializer
    queryset = MMechnoAdExcel.objects.all()
    pagination_class = CustomPagination
