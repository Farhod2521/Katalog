from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    page_size = 24
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'current_page_number': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'items_per_page': len(self.page),
            'results': data
        })


class LimitlessPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'current_page_number': self.page.number,
            'total_pages': self.page.paginator.num_pages,
            'items_per_page': len(self.page),
            'count': self.page.paginator.count,
            'results': data
        })