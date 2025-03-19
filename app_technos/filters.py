from rest_framework.filters import BaseFilterBackend
import coreapi


class TechnoSearchFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name='key',
                location='query',
                required=True,
                type='string',
                description='Column names: volume, category, group, name(search by techno name)',
                ),
            coreapi.Field(
                name='value',
                location='query',
                required=True,
                type='string',
                description='Column value',
                )
            ]
        return fields

    def filter_queryset(self, request, queryset, view):
        return queryset