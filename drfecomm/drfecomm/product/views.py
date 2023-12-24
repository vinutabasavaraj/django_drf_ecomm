from django.shortcuts import render
from drf_spectacular.views import extend_schema
from rest_framework import viewsets
from rest_framework.response import Response

from .models import Category, Brand, Product
from .serializer import CategorySerializer, BrandSerializer, ProductSerializer


class CategoryViewSet(viewsets.ViewSet):
    '''
    A Simple Viewset to view all the categories
    '''

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)
    

class BrandViewSet(viewsets.ViewSet):
    '''
    A Simple Viewset to view all the Brands
    '''

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ViewSet):
    '''
    A Simple Viewset to view all the Products
    '''

    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)

