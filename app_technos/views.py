from rest_framework import permissions
# from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView


import jwt, datetime
from users.models import CatalogUsers
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from app_company.models import Companies

from config.pagination import CustomPagination

from .filters import TechnoSearchFilterBackend

from .models import TechnoVolumes, TechnoCategories, TechnoGroups, Techno, TechnoAllInfo, TechnoAds
from .serializers import (
    TechnoVolumesSerializer, TechnoCategoriesSerializer, TechnoGroupsSerializer, TechnoSerializer, TechnoAllInfoSerializer,
    TechnoAdsSerializer, TechnoAdsDeactivateSerializer, TechnoAdsManageSerializer
    )

# Create your views here.

# APIs for working with TechnoAllINFO
class TechnoInfoDetailView(RetrieveAPIView):
    queryset = Techno.objects.all()
    serializer_class = TechnoSerializer


# APIs for working with TechnoAds
class TechnoAdsFilterByNameAPIListView(ListAPIView):
    serializer_class = TechnoAdsSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        keyword = self.kwargs['csr_code']
        if 'sort_by' in self.request.GET:
            col_name = self.request.GET['sort_by']
        else:
            col_name = 'techno_updated_date'
        queryset = TechnoAds.objects.filter(techno_status=True, techno_name=keyword, company_name__isnull=False).order_by(col_name)

        if 'region' in self.request.GET:
            queryset = queryset.filter(techno_region=self.request.GET['region'])

        if 'district' in self.request.GET:
            queryset = queryset.filter(techno_district=self.request.GET['district'])

        return queryset


class TechnoAdsFilterByUserAPIListView(ListAPIView):
    serializer_class = TechnoAdsSerializer
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
            col_name = '-techno_updated_date'

        queryset = TechnoAds.objects.filter(techno_status=True, company_stir=user_stir).order_by(col_name)

        return queryset


class TechnoUniversalEndpointListView(ListAPIView):
    serializer_class = TechnoAllInfoSerializer
    pagination_class = CustomPagination
    filter_backends = (TechnoSearchFilterBackend,)
    def get_queryset(self):
        col_name = self.request.GET['key']
        
        if 'sort_by' in self.request.GET:
            col_order = self.request.GET['sort_by']
        else:
            col_order = 'techno_name'
        
        if col_name == 'views_count':
            queryset = TechnoAllInfo.objects.all().order_by('-techno_views_count')
        elif col_name == 'volume':
            col_value = self.request.GET['value']
            queryset = TechnoAllInfo.objects.filter(techno_volume=col_value).order_by(col_order)
        elif col_name == 'category':
            col_value = self.request.GET['value']
            queryset = TechnoAllInfo.objects.filter(techno_category=col_value).order_by(col_order)
        elif col_name == 'group':
            col_value = self.request.GET['value']
            queryset = TechnoAllInfo.objects.filter(techno_group=col_value).order_by(col_order)
        elif col_name == 'name':
            col_value = self.request.GET['value']
            queryset = TechnoAllInfo.objects.filter(techno_name__icontains=col_value).order_by(col_order)
        else:
            queryset = TechnoAllInfo.objects.none()
            # return {['result': 'error', 'cause': 'Query params incorrect']}
        return queryset




class TechnoAdsManageView(APIView):
    def post(self, request):
        token = request.META['HTTP_TOKEN']

        if not token:
            raise AuthenticationFailed('Invalid token, login again, please')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        
        # request.data['techno_owner'] = payload['id']
        request.data['company_stir'] = payload['company_stir']
        request.data['company_name'] = payload['company_name']

        serializer = TechnoAdsManageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TechnoAdsDeactivateView(UpdateAPIView):
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
            TechnoAds.objects.filter(id=post_id, company_stir=user_stir).update(techno_status=False, techno_deactivated_date=datetime.datetime.now())
            return Response(data="{'result': 'success', 'description': 'E‘lon muvaffaqiyatli o‘chirildi!'}")
        except Exception as e:
            return Response(data="{'result': 'error', 'description': str(e)}")
