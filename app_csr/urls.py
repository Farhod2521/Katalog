from django.urls import path

from .views import (
    # CSRVolumesListView,
    # CSRPartsListView,
    # CSRChaptersListView,
    # CSRGroupsListView,
    # CSRResourcesListView,
    # CSRResourcesSearchView,
    CSRUniversalEndpointListView,
    CSRFilteredResourcesListView,
)

urlpatterns = [
    path('resources/', CSRFilteredResourcesListView.as_view()),
    path('', CSRUniversalEndpointListView.as_view()),
    # path('volumes/', CSRVolumesListView.as_view()),
    # path('parts/<int:volume_id>/', CSRPartsListView.as_view()),
    # path('chapters/<int:part_id>/', CSRChaptersListView.as_view()),
    # path('groups/<int:chapter_id>/', CSRGroupsListView.as_view()),
    # path('resources/<int:group_id>/', CSRResourcesListView.as_view()),
    # path('resources/search/<str:key_word>/', CSRResourcesSearchView.as_view()),
    # # path('c/<int:pk>/', ProductCategoriesAPIListView.as_view()),
    # # path('g/<int:pk>/', ProductGroupsAPIListView.as_view()),
    # # path('p/<int:pk>/', ProductAPIListView.as_view()),
]