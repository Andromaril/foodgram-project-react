from rest_framework.pagination import PageNumberPagination


class PageSizeNumberPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
