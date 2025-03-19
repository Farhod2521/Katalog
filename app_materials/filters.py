from rest_framework.filters import BaseFilterBackend
import coreapi


class MaterialSearchFilterBackend(BaseFilterBackend):
    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name='key',
                location='query',
                required=True,
                type='string',
                description='Coluumn names: volume, category, group, name(search by material name)',
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