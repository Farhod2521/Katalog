from rest_framework.filters import BaseFilterBackend
import coreapi


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
                ),
            coreapi.Field(
                name='test',
                location='body',
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
                queryset = queryset.filter(resource_url__icontains=r_type, resource_name__icontains=key_word)
            else:
                key_word = request.query_params['value']
                queryset = queryset.filter(resource_name__icontains=key_word)
        except KeyError:
            # no query parameters
            pass
        return queryset