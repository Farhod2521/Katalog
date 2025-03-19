from rest_framework import permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, UpdateAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from config.pagination import CustomPagination

from .models import WorkCategories, WorkGroups, Work, WorkAllInfo, WorkAds
from .serializers import WorkCategoriesSerializer, WorkAdsManageSerializer, WorkGroupsSerializer, WorkSerializer, WorkAllInfoSerializer, WorkAdsSerializer, WorkAdsDeactivateSerializer
from rest_framework.views import APIView
# Create your views here.
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
import jwt, datetime
# APIs for working with Work
class WorkInfoDetailView(RetrieveAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer


# APIs for working with WorkAllINFO
class WorkAdsFilterByNameAPIListView(ListAPIView):
    serializer_class = WorkAdsSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        keyword = self.kwargs['csr_code']
        if self.request.GET['sort_by']:
            col_name = self.request.GET['sort_by']
        else:
            col_name = 'work_updated_date'
        queryset = WorkAds.objects.filter(work_status=True, work_name=keyword, company_name__isnull=False).order_by(col_name)


class WorkUniversalEndpointListView(ListAPIView):
    serializer_class = WorkAllInfoSerializer
    pagination_class = CustomPagination
    def get_queryset(self):
        col_name = self.request.GET['key']
        
        if 'sort_by' in self.request.GET:
            col_order = self.request.GET['sort_by']
        else:
            col_order = 'work_name'
        
        if col_name == 'views_count':
            queryset = WorkAllInfo.objects.all().order_by('-work_views_count')
        elif col_name == 'category':
            col_value = self.request.GET['value']
            queryset = WorkAllInfo.objects.filter(work_category=col_value).order_by(col_order)
        elif col_name == 'group':
            col_value = self.request.GET['value']
            queryset = WorkAllInfo.objects.filter(work_group=col_value).order_by(col_order)
        elif col_name == 'name':
            col_value = self.request.GET['value']
            queryset = WorkAllInfo.objects.filter(work_name__icontains=col_value).order_by(col_order)
        else:
            queryset = WorkAllInfo.objects.none()
        return queryset
    

class WorkAdsManageView(APIView):
    def post(self, request):
        token =  request.META['HTTP_TOKEN']
        if not token:
            raise AuthenticationFailed("Invalid token, Login agian please")
        
        try:
            payload =  jwt.decode(token, 'secret', algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Token expired, login again, please')
        

        request.data['company_stir'] =  payload['company_stir']
        request.data['company_name'] =  payload['company_name']
        serializer =  WorkAdsManageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    



class WorkAdsFilterByUserAPIlistView(ListAPIView):
    serializer_class  = WorkAdsSerializer
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
            col_name = '-work_updated_date'

        queryset = WorkAds.objects.filter(work_status=True, company_stir=user_stir).order_by(col_name)

        return queryset





        
class WorkAdsUpdateView(RetrieveUpdateAPIView):
    serializer_class = WorkAdsManageSerializer
    queryset = WorkAds.objects.all()
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
            work_ads = self.queryset.get(id=pk)
            serializer =  self.get_serializer(work_ads)
            return Response(serializer.data)
        except WorkAds.DoesNotExist:
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
        serializer.save(work_updated_date=datetime.datetime.now())
        return Response(
            data={
                "result": "Success",
                "des": "Baza muvfaqiyatli saqlandi!"
            }
        )
class WorkAdsDeleteView(UpdateAPIView):
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
            WorkAds.objects.get(id=post_id, company_stir=user_stir).delete()
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
