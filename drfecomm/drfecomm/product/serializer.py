from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Brand, Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    class Meta:
        model = Product
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(default="username")
    password = serializers.CharField(default="password")

    class Meta(object):
        model = User
        fields = ['id', 'username', 'password', 'email']

    # def create(self, validated_data):
    #     user = User(
    #         email=validated_data['email'],
    #         username=validated_data['username']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField(default="username")
    password = serializers.CharField(default="password")

    class Meta(object):
        model = User
        fields = ['id', 'username', 'password']

    # def create(self, validated_data):
    #     user = User(
    #         username=validated_data['username']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

# from rest_framework_simplejwt.tokens import RefreshToken, TokenError

# class LogoutSerializer(serializers.Serializer):
#     refresh_token=serializers.CharField()

#     default_error_message = {
#         'bad_token': ('Token is expired or invalid')
#     }

#     def validate(self, attrs):
#         self.token = attrs.get('refresh_token')

#         return attrs

#     def save(self, **kwargs):
#         try:
#             token=RefreshToken(self.token)
#             token.blacklist()
#         except TokenError:
#             return self.fail('bad_token')