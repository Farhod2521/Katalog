from rest_framework import permissions
from urllib.parse import unquote
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from urllib.parse import unquote

from django.db.models import Q

import json
from django.http import HttpResponse, HttpResponseNotFound

from config.pagination import CustomPagination, LimitlessPagination

from .models import CSRVolumes, CSRParts, CSRChapters, CSRGroups, CSRResources, CSRResourcesAllInfos
from .serializers import (
    CSRVolumesSerializer,
    CSRPartsSerializer,
    CSRChaptersSerializer,
    CSRGroupsSerializer,
    CSRResourcesSerializer,
    CSRAllInfoSerializer
)

# class CSRVolumesListView(ListAPIView):
#     queryset = CSRVolumes.objects.all().order_by('volume_code')
#     serializer_class = CSRVolumesSerializer


# class CSRPartsListView(ListAPIView):
#     serializer_class = CSRPartsSerializer
#     def get_queryset(self):
#         queryset = CSRParts.objects.filter(part_volume=self.kwargs['volume_id']).order_by('part_code')
#         return queryset


# class CSRChaptersListView(ListAPIView):
#     serializer_class = CSRChaptersSerializer
#     def get_queryset(self):
#         queryset = CSRChapters.objects.filter(chapter_part=self.kwargs['part_id']).order_by('chapter_code')
#         return queryset


# class CSRGroupsListView(ListAPIView):
#     serializer_class = CSRGroupsSerializer
#     def get_queryset(self):
#         queryset = CSRGroups.objects.filter(group_chapter=self.kwargs['chapter_id']).order_by('group_code')
#         return queryset


# class CSRResourcesListView(ListAPIView):
#     serializer_class = CSRResourcesSerializer
#     def get_queryset(self):
#         queryset = CSRResources.objects.filter(resource_group=self.kwargs['group_id']).order_by('resource_code')
#         return queryset


# class CSRResourcesSearchView(ListAPIView):
#     serializer_class = CSRAllInfoSerializer
#     def get_queryset(self):
#         tvar_url = self.kwargs['key_word']
#         fk = unquote(tvar_url)
#         queryset = CSRResourcesAllInfos.objects.filter(resource_name__icontains=fk).order_by('resource_name')
#         return queryset


class CSRUniversalEndpointListView(ListAPIView):
    pagination_class = LimitlessPagination
    def get_serializer_class(self):
        table_name = self.request.GET['key']
        
        if table_name == 'volumes':
            serializer_class = CSRVolumesSerializer
        elif table_name == 'parts':
            serializer_class = CSRPartsSerializer
        elif table_name == 'chapters':
            serializer_class = CSRChaptersSerializer
        elif table_name == 'groups':
            serializer_class = CSRGroupsSerializer
        elif table_name == 'resources':
            serializer_class = CSRAllInfoSerializer
        elif table_name == 'name':
            serializer_class = CSRAllInfoSerializer
        else:
            serializer_class = CSRVolumesSerializer
        
        return serializer_class
    
    def get_queryset(self):
        table_name = self.request.GET['key']
        
        if table_name == 'volumes':
            queryset = CSRVolumes.objects.all().order_by('id')
        elif table_name == 'parts':
            fk = self.request.GET['parent']
            queryset = CSRParts.objects.filter(part_volume=fk).order_by('id')
        elif table_name == 'chapters':
            fk = self.request.GET['parent']
            queryset = CSRChapters.objects.filter(chapter_part=fk).order_by('id')
        elif table_name == 'groups':
            fk = self.request.GET['parent']
            queryset = CSRGroups.objects.filter(group_chapter=fk).order_by('id')
        elif table_name == 'resources':
            if 'parent' in self.request.GET:
                fk = self.request.GET['parent']
                queryset = CSRResourcesAllInfos.objects.filter(resource_group=fk).order_by('id')
            else:
                queryset = CSRResourcesAllInfos.objects.all().order_by('resource_name')
        elif table_name == 'name':
            key_word = self.request.GET['parent']
            if '.' in key_word:
                queryset = CSRResourcesAllInfos.objects.filter(resource_code__icontains=key_word).order_by('resource_name')
            else:
                queryset = CSRResourcesAllInfos.objects.filter(resource_name__icontains=key_word).order_by('resource_name')
                if len(queryset) == 0 and " " in key_word or "%20" in key_word:
                    key_word = unquote(key_word)
                    keywordlar = key_word.split(" ")
                    
                    queryx = Q()
    
                    for x in keywordlar:
                      queryx &= Q(resource_name__icontains=x)
                    
                    queryset = CSRResourcesAllInfos.objects.filter(queryx)
        else:
            queryset = CSRVolumes.objects.none()
        return queryset



class CSRFilteredResourcesListView(ListAPIView):
    serializer_class = CSRAllInfoSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        col_name = self.request.GET['key']
        
        if 'sort_by' in self.request.GET:
            col_order = self.request.GET['sort_by']
        else:
            col_order = 'resource_code'
        
        # if col_name == 'views_count':
        #     queryset = CSRResourcesAllInfos.objects.all().order_by('-resource_views_count')
        if col_name == 'volume':
            col_value = self.request.GET['value']
            queryset = CSRResourcesAllInfos.objects.filter(resource_volume=col_value).order_by(col_order)
        elif col_name == 'part':
            col_value = self.request.GET['value']
            queryset = CSRResourcesAllInfos.objects.filter(resource_part=col_value).order_by(col_order)
        elif col_name == 'chapter':
            col_value = self.request.GET['value']
            queryset = CSRResourcesAllInfos.objects.filter(resource_chapter=col_value).order_by(col_order)
        elif col_name == 'group':
            col_value = self.request.GET['value']
            queryset = CSRResourcesAllInfos.objects.filter(resource_group=col_value).order_by(col_order)
        elif col_name == 'name':
            col_value = self.request.GET['value']
            queryset = CSRResourcesAllInfos.objects.filter(resource_name__icontains=col_value).order_by(col_order)
        else:
            queryset = CSRResourcesAllInfos.objects.none()
        return queryset