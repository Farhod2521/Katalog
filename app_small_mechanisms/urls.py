from django.urls import path
# from rest_framework.routers import SimpleRouter

from .views import (
    SmallMechanoInfoDetailView,
    SmallMechanoAdsFilterByUserAPIListView,
    SmallMechanoAdsFilterByNameAPIListView,
    SmallMechanoUniversalEndpointListView,
    SmallMechanoAdsManageView,
    SmallMechanoAdsDeactivateView,
    SmallMechanoAdsUpdateView,
    SmallMechanoAdsDeleteView

    
)

urlpatterns = [
    path('update/<int:pk>/', SmallMechanoAdsUpdateView.as_view()),
    path('ads/delete', SmallMechanoAdsDeleteView.as_view()),
    path('ads/add/new', SmallMechanoAdsManageView.as_view()),
    path('ads/my/', SmallMechanoAdsFilterByUserAPIListView.as_view()),
    path('ads/deactivate', SmallMechanoAdsDeactivateView.as_view()),
    path('ads/<str:csr_code>/', SmallMechanoAdsFilterByNameAPIListView.as_view()),
    path('<str:pk>/', SmallMechanoInfoDetailView.as_view()),
    path('', SmallMechanoUniversalEndpointListView.as_view()),
    

]
