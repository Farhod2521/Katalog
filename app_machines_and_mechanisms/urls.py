from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    MMechanoInfoDetailView,
    MMechnoAdsUpdateView,
    MMechnoAdsDeleteView,

    MMechanoAdsFilterByNameAPIListView,
    MMechanoAdsFilterByUserAPIListView, 
    MMechanoUniversalEndpointListView,
    MMechanoAdsManageView,
    MMechanoAdsDeactivateView,
    MMechnoAdExcelListApiview,
    
)

urlpatterns = [
    path('mmechno/2023/', MMechnoAdExcelListApiview.as_view()),
    path('update/<int:pk>/', MMechnoAdsUpdateView.as_view()),
    path('ads/deactivate', MMechnoAdsDeleteView.as_view()),
    path('ads/add/new', MMechanoAdsManageView.as_view()),
    path('ads/my/', MMechanoAdsFilterByUserAPIListView.as_view()),
    path('ads/deactivate', MMechanoAdsDeactivateView.as_view()),
    path('ads/<str:csr_code>/', MMechanoAdsFilterByNameAPIListView.as_view()),
    path('<str:pk>/', MMechanoInfoDetailView.as_view()),
    path('', MMechanoUniversalEndpointListView.as_view()),
    

]
