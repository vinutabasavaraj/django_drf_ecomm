from django.shortcuts import get_object_or_404, render
from drf_spectacular.views import extend_schema
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.contrib.auth.models import User

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


from .models import Category, Brand, Product
from .serializer import CategorySerializer, BrandSerializer, ProductSerializer, UserSerializer, LoginSerializer

class RegisterViewSet(viewsets.ViewSet):
    """
    A Simple Viewset for Register the User
    """
    @extend_schema(request=UserSerializer,responses=UserSerializer, tags=['Login'])
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username = request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            return Response({"message" : "User Created Successfully",'userId': serializer.data["id"],'userName':serializer.data["username"], 'userEmail':serializer.data["email"]}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginViewSet(viewsets.ViewSet):
    """
    A Simple Viewset for Login
    """
    @extend_schema(request=LoginSerializer, responses=UserSerializer, tags=['Login'])
    def create(self, request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({"message":"Invalid password"}, status=status.HTTP_404_NOT_FOUND)
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response({"message" : "Logged In Successfully",
        'refresh': str(refresh),'access': str(refresh.access_token), 'userId': serializer.data["id"],'username':serializer.data["username"], 'useremail':serializer.data["email"] })

class CategoryViewSet(viewsets.ViewSet):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer, tags=['Category'], parameters=[
        OpenApiParameter(name='offset', description='offset value', 
                         required=False, type=int),
    ],
)
    def list(self, request):
        '''
            A Simple Viewset to view all the categories
        '''
        offset = request.query_params.get('offset')
        print(offset)
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)
    

    @extend_schema(request=CategorySerializer, responses=CategorySerializer, tags=['Category'])
    def create(self, request):
        '''
            A Simple Viewset to create category
        '''
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    
    @extend_schema(responses=CategorySerializer, tags=['Category'])
    def retrieve(self, request, pk=None):
        '''
            A Simple Viewset to view particular category
        '''
        try:
            queryset_val = Category.objects.get(id=pk)
        except Exception as e:
             return Response(
            {"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
        if queryset_val:
            serializer = CategorySerializer(queryset_val, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        

class BrandViewSet(viewsets.ViewSet):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer, tags=['Brand'])
    def list(self, request):
        '''
            A Simple Viewset to view all the Brands
        '''
        serializer = BrandSerializer(self.queryset, many=True)
        return Response(serializer.data)

class ProductViewSet(viewsets.ViewSet):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
   
    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer, tags=['Product'])
    def list(self, request):
        '''
        A Simple Viewset to view all the Products
        '''

        serializer = ProductSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    






