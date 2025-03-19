from django.urls import path
# from rest_framework.routers import SimpleRouter

from .views import (
    MaterialsAdsFilterByNameAPIListView,
    MaterialsAdsFilterByUserAPIListView,
    MaterialsUniversalEndpointListView,
    MaterialsInfoDetailView,
    # MaterialAdsViewSet
    MaterialAdsManageView,
    MaterialAdsDeactivateView,
    MaterialAdsUpdateView,ExcelExportView, MaterialAdsList, MaterialRegionCompanyStir,MaterialAdsViewSet11
)

# router = SimpleRouter()
# router.register('manage', MaterialAdsViewSet, basename='material_ads_manage')

urlpatterns = [
    path('company/elon/', MaterialAdsViewSet11.as_view()),
    path('ads/add/new', MaterialAdsManageView.as_view()),
    path('ads/deactivate', MaterialAdsDeactivateView.as_view()),
    path('ads/my/', MaterialsAdsFilterByUserAPIListView.as_view()),
    path('ads/<str:csr_code>/', MaterialsAdsFilterByNameAPIListView.as_view()),
    path('<str:pk>/', MaterialsInfoDetailView.as_view()),
    path('', MaterialsUniversalEndpointListView.as_view()),
    path('update/<int:pk>/', MaterialAdsUpdateView.as_view()),
    path('export/excel/', ExcelExportView.as_view(), name='excel_export'),
    path('api/elon/', MaterialAdsList.as_view()),
    path('region_filter/<str:region>/',MaterialRegionCompanyStir.as_view()),

]# + router.urls
