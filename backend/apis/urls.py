from django.urls import path
from .views import getRoutes, RegisterView, LoginView, logoutView, testView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', getRoutes, name='get_routes'),
    path('login/', LoginView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logoutView, name='logout'),
    path('test/', testView, name='test_route'),
]


