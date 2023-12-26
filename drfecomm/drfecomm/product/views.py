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
from .pagination import CategoryList
# from django.urls import re_path as url
# from rest_framework_swagger.views import get_swagger_view
# schema_view = get_swagger_view(title='Django DRF APIs', url='/http://localhost:8000/api/schema/docs/#/')

# schema_view = get_swagger_view(title='Django DRF Ecommerece')

# urlpatterns = [
#     url(r'^$', schema_view)
# ]

class RegisterViewSet(viewsets.ViewSet):
    """
    A Simple Viewset for Register the User
    """
    @extend_schema(request=UserSerializer,responses=UserSerializer, tags=['Login'])
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = User.objects.filter(username=request.data['username']).exists()
            useremail = User.objects.filter(email=request.data['email']).exists()
            if username:
                return Response({"message": "Username already exists"}, status=status.HTTP_409_CONFLICT)
            elif useremail:
                return Response({"message": "email already exists"}, status=status.HTTP_409_CONFLICT)
            serializer.save()
            user = User.objects.get(username = request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            return Response({'message' : "User Created Successfully",'userId': serializer.data["id"],'userName':serializer.data["username"], 'userEmail':serializer.data["email"]}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginViewSet(viewsets.ViewSet):
    """
    A Simple Viewset for Login
    """
    @extend_schema(request=LoginSerializer, responses=UserSerializer, tags=['Login'])
    def create(self, request):
        try:
            user = User.objects.get(username=request.data['username'] or user.check_password(request.data['password']))
        except Exception as e:
             return Response(
            {"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
    
        refresh = RefreshToken.for_user(user)
        serializer = UserSerializer(user)
        return Response({"message" : "Logged In Successfully",
        'refresh': str(refresh),'access': str(refresh.access_token), 'userId': serializer.data["id"],'username':serializer.data["username"], 'useremail':serializer.data["email"] })

class CategoryViewSet(viewsets.ViewSet):
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,]
    pagination_class = CategoryList
    
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
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(self.queryset, request)
        
        serializer = CategorySerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response({"data": serializer.data})
        # serializer = CategorySerializer(self.queryset, many=True)
        # return Response({"data" : serializer.data} )
    

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
    
# from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken


# class LogoutViewSet(viewsets.ViewSet):
#     """
#     A Simple Viewset for Logout the User
#     """
   
#     @extend_schema(tags=['Logout'])
#     def create(self, request):    
       
#         token = RefreshToken(request.data.get('refresh'))

#         token.blacklist()
#         return Response({"message": "Logged Out"}, status=status.HTTP_200_OK)
        
        # print(token)
        # token.delete()
            # try:
        #     refresh_token = request.data.get('refresh_token')
        #     print("refresh_token ",refresh_token)
        #     # token = request.META['HTTP_AUTHORIZATION']
        #     # print("token", token)
        #     token_obj = RefreshToken(refresh_token)
        #     token_obj.blacklist()  # Use blacklist() method to invalidate the token
        #     
        # except Exception as err:
        #     return Response({"message": str(err)}, status=status.HTTP_400_BAD_REQUEST)





