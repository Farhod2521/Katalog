from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import (
    VolumesListView, CategoriesListView, GroupsListView, CustomLanguagesListView, GetMenuTranslations,
    SelectedThingsSelectView, SelectedThingsListView, SelectedThingsDeSelect, SearchedResourcesListView,
    getCurrencyCources, getStatistics, BirjaAPIView, SoliqAPIView, EHRequestView, 
    EH_DataAPIView, getCertificate, BojxonaBulkCreateAPIView, BojxonaListApiView2, 
    TexnikJTSAListApiView, CreateMultiplePosts, IQTISODMOLIYAVAZRILIKListApiView, ConstructionDataView,
    DocumentCategoryCreateView, DocumentCreateView, DocumentListView, Material_Soliq_PriceListView
)

urlpatterns = [
    path('volumes/', VolumesListView.as_view()),
    path('categories/', CategoriesListView.as_view()),
    path('groups/', GroupsListView.as_view()),
    # path('translations/', CustomLanguagesListView.as_view()),
    path('translations/', GetMenuTranslations, name='menu_translate'),
    path('selecteds/', SelectedThingsListView.as_view()),
    path('selecteds/select/', SelectedThingsSelectView.as_view()),
    path('selecteds/deselect/<int:pk>/', SelectedThingsDeSelect, name='deselect'),
    path('currency/', getCurrencyCources, name='currency'),
    # API for Search bar, HEADER
    path('search/', SearchedResourcesListView.as_view()),
    # API for statistics
    path('stat/', getStatistics, name='stat'),
    path('api_birja/', BirjaAPIView.as_view(), name='birja-api'),
    path('soliq/', SoliqAPIView.as_view(), name='soliq'),
    path('eh-request/', EHRequestView.as_view(), name='token_request'),
    path('eh-data/', EH_DataAPIView.as_view(), name='tokendata'),
    path('certificate/', getCertificate, name='cert'),
    path('bojxona/bulk-create/', BojxonaBulkCreateAPIView.as_view(), name='bojxona-bulk-create'),
    path('bojxona/list/', BojxonaListApiView2.as_view(), name='bojxona-bulk-create'),
    path('texnikjtsa/list/', TexnikJTSAListApiView.as_view(), name='bojxona-bulk-create'),
    path('iqtisod/', CreateMultiplePosts.as_view(), name='create_multiple_posts'),
    path('iqtisod_list/', IQTISODMOLIYAVAZRILIKListApiView.as_view(), name='create_multiple_posts'),
    path('api/construction/certifikat/', ConstructionDataView.as_view(), name='construction-view'),

    path('document-category/create/', DocumentCategoryCreateView.as_view(), name='document-category-create'),
    path('document/create/', DocumentCreateView.as_view(), name='document-create'),
    path('document/list/', DocumentListView.as_view(), name='document-create'),

    path('soliq_data_price/', Material_Soliq_PriceListView.as_view(), name='document-create'),

]
