from django.shortcuts import render
from drf_spectacular.views import extend_schema
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated



from .models import Category, Brand, Product
from .serializer import CategorySerializer, BrandSerializer, ProductSerializer, UserSerializer, LoginSerializer

class CategoryViewSet(viewsets.ViewSet):
    '''
    A Simple Viewset to view all the categories
    '''
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer, tags=['Category'], parameters=[
        OpenApiParameter(name='offset', description='offset value', 
                         required=False, type=int),
    ],
)
    def list(self, request):
        offset = request.query_params.get('offset')
        print(offset)
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)
    

    @extend_schema(request=CategorySerializer, responses=CategorySerializer, tags=['Category'])
    def create(self, request):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        # category_val = Category(category='new cat')
        # category_val.save()
    
    @extend_schema(responses=CategorySerializer, tags=['Category'])
    def retrieve(self, request, pk=None):
        try:
            queryset_val = Category.objects.get(id=pk)
        except Exception as e:
             return Response(
            {"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        if queryset_val:
            serializer = CategorySerializer(queryset_val, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
           


class BrandViewSet(viewsets.ViewSet):
    '''
    A Simple Viewset to view all the Brands
    '''

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer, tags=['Brand'])
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ViewSet):
    '''
    A Simple Viewset to view all the Products
    '''

    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer, tags=['Product'])
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    

# class LoginViewSet(viewsets.ViewSet):
#     """
#     A Simple Viewset for Login
#     """
#     @extend_schema(request=LoginSerializer, responses=UserSerializer, tags=['Login'])
#     def create(self, request):
#         user = get_object_or_404(User, username=request.data['username'])
#         if not user.check_password(request.data['password']):
#             return Response("Wrong password", status=status.HTTP_404_NOT_FOUND)
#         token, created = Token.objects.get_or_create(user=user)
#         serializer = UserSerializer(user)
#         return Response({'token': token.key, 'user': serializer.data})


class RegisterViewSet(viewsets.ViewSet):
    """
    A Simple Viewset for Register of User
    """
    @extend_schema(request=UserSerializer,responses=UserSerializer,tags=['Register'])
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username = request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

