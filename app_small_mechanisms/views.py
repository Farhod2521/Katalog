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

from .models import SmallMechanoCategories, SmallMechanoGroups, SmallMechano, SmallMechanoAllInfo, SmallMechanoAds
from .serializers import (
    SmallMechanoCategoriesSerializer, SmallMechanoGroupsSerializer, SmallMechanoSerializer, SmallMechanoAllInfoSerializer,
    SmallMechanoAdsSerializer, SmallMechanoAdsDeactivateSerializer, SmallMechanoAdsManageSerializer 
    )

# Create your views here.

# APIs for working with SmallMechano
class SmallMechanoInfoDetailView(RetrieveAPIView):
    queryset = SmallMechano.objects.all()
    serializer_class = SmallMechanoSerializer

# APIs for working with AllINFO
class SmallMechanoAdsFilterByNameAPIListView(ListAPIView):
    serializer_class = SmallMechanoAdsSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        keyword = self.kwargs['csr_code']
        if 'sort_by' in self.request.GET:
            col_name = self.request.GET['sort_by']
        else:
            col_name = 'smallmechano_updated_date'
        queryset = SmallMechanoAds.objects.filter(smallmechano_status=True, smallmechano_name=keyword, company_name__isnull=False).order_by(col_name)
        return queryset


class SmallMechanoUniversalEndpointListView(ListAPIView):
    serializer_class = SmallMechanoAllInfoSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        col_name = self.request.GET['key']
        
        if 'sort_by' in self.request.GET:
            col_order = self.request.GET['sort_by']
        else:
            col_order = 'smallmechano_name'
        
        if col_name == 'views_count':
            queryset = SmallMechanoAllInfo.objects.all().order_by('-smallmechano_views_count')
        elif col_name == 'category':
            col_value = self.request.GET['value']
            queryset = SmallMechanoAllInfo.objects.filter(smallmechano_category=col_value).order_by(col_order)
        elif col_name == 'group':
            col_value = self.request.GET['value']
            queryset = SmallMechanoAllInfo.objects.filter(smallmechano_group=col_value).order_by(col_order)
        elif col_name == 'name':
            col_value = self.request.GET['value']
            queryset = SmallMechanoAllInfo.objects.filter(smallmechano_name__icontains=col_value).order_by(col_order)
        else:
            queryset = SmallMechanoAllInfo.objects.none()
        return queryset




class SmallMechanoAdsManageView(APIView):
    def post(self, request):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        #request.data['smallmechano_owner'] = payload['id']
        request.data['company_stir'] = payload['company_stir']
        company = Companies.objects.filter(pk=payload['company_stir']).first()
        request.data['company_name'] = company.company_name
        
        serializer = SmallMechanoAdsManageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class SmallMechanoAdsDeactivateView(UpdateAPIView):
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
            SmallMechanoAds.objects.filter(id=post_id, smallmechano_owner=user_id).update(smallmechano_status=False, smallmechano_deactivated_date=datetime.datetime.now())
            return Response(data="{'result': 'success', 'description': 'E‘lon muvaffaqiyatli o‘chirildi!'}")
        except Exception as e:
            return Response(data="{'result': 'error', 'description': str(e)}")
        

class SmallMechanoAdsFilterByUserAPIListView(ListAPIView):
    serializer_class = SmallMechanoAdsSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        token = self.request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            user_stir = payload['company_stir']
            print(user_stir)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        if 'sort_by' in self.request.GET:
            col_name = self.request.GET['sort_by']
        else:
            col_name = '-smallmechano_updated_date'
        
        queryset = SmallMechanoAds.objects.filter(smallmechano_status=True, company_stir=user_stir).order_by(col_name)
        
        return queryset

    

class SmallMechanoAdsUpdateView(RetrieveUpdateAPIView):
    serializer_class = SmallMechanoAdsManageSerializer
    queryset = SmallMechanoAds.objects.all()
    http_method_names  = ['get', 'put']

    def retrieve(self, request, pk=None):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
           payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please') 
        
        try:
            smallmechano_ads = self.queryset.get(id=pk)
            serializer =  self.get_serializer(smallmechano_ads)
            return Response(serializer.data)
        except SmallMechanoAds.DoesNotExist:
            return Response(
                data={
                    "result": "not found",
                    "description":" SmallMechanoAds not found "
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
        serializer.save(smallmechano_updated_date=datetime.datetime.now())
        return Response(
            data={
                "result": "Success",
                "des": "Baza muvfaqiyatli saqlandi!"
            }
        )
class SmallMechanoAdsDeleteView(UpdateAPIView):
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
            SmallMechanoAds.objects.get(id=post_id, company_stir=user_stir).delete()
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
