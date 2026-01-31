from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'datasets', views.EquipmentDatasetViewSet, basename='dataset')

urlpatterns = [
    # Health check
    path('health/', views.health_check, name='health'),
    
    # Authentication endpoints
    path('auth/register/', views.register_user, name='register'),
    path('auth/login/', views.login_user, name='login'),
    path('auth/logout/', views.logout_user, name='logout'),
    
    # Dataset endpoints (via router)
    path('', include(router.urls)),
]
