from django.urls import path

from .views import UzbTerritoriesListView, Company_Infarmation, CompaniesListView, CompanyDetailView, CompanyAdsAPIListView, Company_Region_Filter, Company_Info_UpdateView


urlpatterns = [
    path('company_info_update/', Company_Info_UpdateView.as_view()),
    path('territories/', UzbTerritoriesListView.as_view()),
    path('ads/<str:stir>/', CompanyAdsAPIListView.as_view()),
    path('company_info/', Company_Infarmation.as_view()), 
    path('<str:pk>/', CompanyDetailView.as_view()),
    path('', CompaniesListView.as_view()),
    path('region_filter/<str:region>/',Company_Region_Filter.as_view()),
      
]
