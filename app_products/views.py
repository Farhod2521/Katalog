from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import ProductVolumes, ProductCategories, ProductGroups, Product, ProductAllInfo, ProductAds
from .serializers import ProductVolumesSerializer, ProductCategoriesSerializer, ProductGroupsSerializer, ProductSerializer, ProductAllInfoSerializer, ProductAdsSerializer, ProductAdsDeactivateSerializer

# Create your views here.

# APIs for working with Product's volumes
class ProductVolumesAPIListView(ListAPIView):
    queryset = ProductVolumes.objects.all().order_by('id')
    serializer_class = ProductVolumesSerializer


# APIs for working with Product's categories
class ProductCategoriesAPIListView(ListAPIView):
    serializer_class = ProductCategoriesSerializer
    def get_queryset(self):
        fk = self.kwargs['pk']
        queryset = ProductCategories.objects.filter(category_volume=fk).order_by('category_name')
        return queryset


# APIs for working with Product's groups
class ProductGroupsAPIListView(ListAPIView):
    serializer_class = ProductGroupsSerializer
    def get_queryset(self):
        fk = self.kwargs['pk']
        queryset = ProductGroups.objects.filter(group_category=fk).order_by('group_name')
        return queryset


# APIs for working with Product
class ProductAPIListView(ListAPIView):
    serializer_class = ProductSerializer
    def get_queryset(self):
        fk = self.kwargs['pk']
        queryset = Product.objects.filter(product_group=fk).order_by('product_name')
        return queryset


# APIs for working with ProductAllINFO
class ProductSearchByNameAPIListView(LoginRequiredMixin, ListAPIView):
    serializer_class = ProductAllInfoSerializer
    def get_queryset(self):
        keyword = self.kwargs['key_word']
        queryset = ProductAllInfo.objects.filter(product_name__icontains=keyword).order_by('product_name')
        return queryset


# APIs for working with ProductAds
class ProductAdsListViewSet(ModelViewSet):
    # pagination_class =
    http_method_names = ['get']
    queryset = ProductAds.objects.filter(product_status=True).order_by('id')
    serializer_class = ProductAdsSerializer

class ProductAdsViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'put', 'patch']
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ProductAds.objects.filter(product_status=True).order_by('id')
    serializer_class = ProductAdsSerializer

class ProductAdsDeactivateViewSet(ModelViewSet):
    http_method_names = ['patch']
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ProductAds.objects.filter(product_status=True).order_by('id')
    serializer_class = ProductAdsDeactivateSerializer