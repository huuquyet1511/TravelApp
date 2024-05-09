from rest_framework.pagination import PageNumberPagination


class TourPaginator(PageNumberPagination):
    page_size = 2


class NewsPaginator(PageNumberPagination):
    page_size = 2