from . import views
from django.urls import path
from .views import AddEmployeeView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

app_name = 'api'

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name="register"),
    path('login/',views.LoginAPIView.as_view(),name="login"),
    path('logout/', views.LogoutAPIView.as_view(), name="logout"),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('send-otp/', views.send_otp, name='send-otp'),
    path('confirm-otp/', views.confirm_otp, name='confirm-otp'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('add-employee/', AddEmployeeView.as_view(), name='add-employee'),
]