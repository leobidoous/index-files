from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response


class CustomPagination(LimitOffsetPagination):
    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_size': self.default_limit,
            'offset': self.offset,
            'count': self.count,
            'results': data
        })


class LargeResultsSetPagination(CustomPagination):
    default_limit = 1000
    max_limit = 10000


class DefaultResultsSetPagination(CustomPagination):
    default_limit = 10
    max_limit = 100
