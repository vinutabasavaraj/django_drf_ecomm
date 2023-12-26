from rest_framework.pagination import PageNumberPagination

class CategoryList(PageNumberPagination):
    page_size = 5