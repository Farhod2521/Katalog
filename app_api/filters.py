from rest_framework.filters import BaseFilterBackend
import coreapi

from urllib.parse import unquote

from django.db.models import Q

from .models import CustomLanguages, SelectedThings, ResourcesList4Search


resource_types = ['materials', 'machine-mechano', 'small-mechano', 'works', 'techno']


class SelectedThingsFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name='user',
                location='query',
                required=True,
                type='int',
                description='Filter by user',
                ),
            coreapi.Field(
                name='type',
                location='query',
                required=False,
                type='string',
                description='Filter by thing type (company, product, ad, ...)',
                )
            ]
        return fields

    def filter_queryset(self, request, queryset, view):
        try:
            # if 'user' in request.query_params:
            user_id = request.query_params['user']
            queryset = queryset.filter(user=user_id)
            if 'type' in request.query_params:
                type_id = request.query_params['type']
                queryset = queryset.filter(thing_type=type_id)
        except KeyError:
            # no query parameters
            pass
        return queryset


class SearchedThingsFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name='key',
                location='query',
                required=True,
                type='string',
                description='Filter by type',
                ),
            coreapi.Field(
                name='value',
                location='query',
                required=True,
                type='string',
                description='Filter by name, code',
                )
            ]
        return fields

    def filter_queryset(self, request, queryset, view):
        try:
            r_type = request.query_params['key']
            # queryset = queryset.filter(user=user_id)
            if r_type in resource_types:
                key_word = request.query_params['value']
                
                if '.' in key_word:
                    queryset = queryset.filter(resource_url__icontains=r_type, resource_code__icontains=key_word)
                else:
                    queryset = queryset.filter(resource_url__icontains=r_type, resource_name__icontains=key_word) | queryset.filter(resource_url__icontains=r_type, resource_desc__icontains=key_word)
                    
                    if len(queryset) == 0 and " " in key_word or len(queryset) == 0 and "%20" in key_word:
                        key_word = unquote(key_word)
                        keywordlar = key_word.split(" ")
                        
                        queryx = Q()
        
                        for x in keywordlar:
                          queryx &= Q(resource_url__icontains=r_type, resource_name__icontains=x) | Q(resource_url__icontains=r_type, resource_desc__icontains=x)
                        
                        queryset = ResourcesList4Search.objects.filter(queryx)
            else:
                key_word = request.query_params['value']
                
                if '.' in key_word:
                    queryset = queryset.filter(resource_code__icontains=key_word)
                else:
                    queryset = queryset.filter(resource_name__icontains=key_word) | queryset.filter(resource_desc__icontains=key_word)
                    
                    if len(queryset) == 0 and " " in key_word or len(queryset) == 0 and "%20" in key_word:
                        key_word = unquote(key_word)
                        keywordlar = key_word.split(" ")
                        
                        queryx = Q()
        
                        for x in keywordlar:
                          queryx &= Q(resource_name__icontains=x) | Q(resource_desc__icontains=x)
                        
                        queryset = ResourcesList4Search.objects.filter(queryx)
        except KeyError:
            # no query parameters
            queryset = ResourcesList4Search.objects.none()
        return queryset