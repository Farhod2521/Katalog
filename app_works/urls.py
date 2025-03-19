from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    WorkInfoDetailView,
    WorkAdsFilterByUserAPIlistView,
    WorkAdsFilterByNameAPIListView,
    WorkUniversalEndpointListView,
    WorkAdsManageView,
    WorkAdsUpdateView,
    WorkAdsDeleteView,

)

urlpatterns = [
    path('update/<int:pk>/', WorkAdsUpdateView.as_view()),
    path('ads/delete', WorkAdsDeleteView.as_view()),
    path('ads/add/new', WorkAdsManageView.as_view()),
    path('ads/my/', WorkAdsFilterByUserAPIlistView.as_view()),
    path('ads/filter/<str:csr_code>/', WorkAdsFilterByNameAPIListView.as_view()),
    path('<str:pk>/', WorkInfoDetailView.as_view()),
    path('', WorkUniversalEndpointListView.as_view()),
]
