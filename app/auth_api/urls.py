from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from django.http import JsonResponse


urlpatterns = [
    path('', lambda request: JsonResponse({"message": "Auth API root"})),  # default endpoint
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]