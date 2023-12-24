
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from drfecomm.product import views

router = DefaultRouter()
router.register(r"category", views.CategoryViewSet)
router.register(r"brand", views.BrandViewSet)
router.register(r"product", views.ProductViewSet)



urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/', include(router.urls)),
    path(r'api/schema/', SpectacularAPIView.as_view(), name="schema"),  #built-in fun
    path(r'api/schema/docs/', SpectacularSwaggerView.as_view(url_name ="schema")),
]
