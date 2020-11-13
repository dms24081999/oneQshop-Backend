from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


class ProductsLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 25


class ProductsPageNumberPagination(PageNumberPagination):
    page_size = 10
