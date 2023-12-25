
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from drfecomm.product import views

router = DefaultRouter()
router.register(r"category", views.CategoryViewSet, basename="category")
router.register(r"brand", views.BrandViewSet, basename="brand")
router.register(r"product", views.ProductViewSet, basename="product")
router.register(r"login", views.LoginViewSet, basename="login")
router.register(r"register", views.RegisterViewSet, basename="register")




urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/', include(router.urls)),
    path(r'api/schema/', SpectacularAPIView.as_view(), name = "schema"),  #built-in fun
    path(r'api/schema/docs/', SpectacularSwaggerView.as_view(url_name = "schema")),
    # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
