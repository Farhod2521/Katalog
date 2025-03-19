from django.urls import path

from .views import (
    TechnoInfoDetailView,
    TechnoAdsFilterByUserAPIListView,
    TechnoUniversalEndpointListView,
    TechnoAdsFilterByNameAPIListView,
    TechnoAdsManageView,
    TechnoAdsDeactivateView
)

urlpatterns = [
    path('ads/add/new', TechnoAdsManageView.as_view()),
    path('ads/deactivate', TechnoAdsDeactivateView.as_view()),
    path('ads/my/', TechnoAdsFilterByUserAPIListView.as_view()),
    path('ads/<str:csr_code>/', TechnoAdsFilterByNameAPIListView.as_view()),
    path('<str:pk>/', TechnoInfoDetailView.as_view()),
    path('', TechnoUniversalEndpointListView.as_view()),
]