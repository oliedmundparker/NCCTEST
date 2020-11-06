from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'scan', views.ScanViewSet)
router.register(r'user', views.UserViewSet)
router.register(r'assets', views.AssetsViewSet)
router.register(r'vulnerability', views.VulnerabilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]