from django.urls import path 
from .views import CmetaApiView, CmetaCategoryApiView, Sample_ProjectApiView, Sample_ProjectCategoryApiView


urlpatterns = [
    path('cmeta/<int:category_id>/', CmetaApiView.as_view(), name='cmeta-by-category'),
    path("cmeta/category/", CmetaCategoryApiView.as_view()),
    path('sample/<int:category_id>/', Sample_ProjectApiView.as_view(), name='cmeta-by-category'),
    path("sample/category/", Sample_ProjectCategoryApiView.as_view())
]
