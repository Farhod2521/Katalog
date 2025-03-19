from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    ProductVolumesAPIListView,
    ProductCategoriesAPIListView,
    ProductGroupsAPIListView,
    ProductAPIListView,
    ProductSearchByNameAPIListView,
    ProductAdsViewSet,
    ProductAdsDeactivateViewSet,
    ProductAdsListViewSet,
)

router = SimpleRouter()
router.register('ads', ProductAdsListViewSet, basename='product_ads')
router.register('deactivate', ProductAdsDeactivateViewSet, basename='product_ads_deactivate')
router.register('manage', ProductAdsViewSet, basename='product_ads_manage')

urlpatterns = [
    path('v/', ProductVolumesAPIListView.as_view()),
    path('c/<int:pk>/', ProductCategoriesAPIListView.as_view()),
    path('g/<int:pk>/', ProductGroupsAPIListView.as_view()),
    path('p/<int:pk>/', ProductAPIListView.as_view()),
    # path('m/ads/delete/<int:pk>/', .as_view()),
    path('search/<str:key_word>/', ProductSearchByNameAPIListView.as_view()),
] + router.urls