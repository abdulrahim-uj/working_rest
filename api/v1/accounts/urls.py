from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

app_name = 'accounts'

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    path('login/', views.UserLoginApiView.as_view(), name="loginUser"),
    path('logout/', views.UserLogoutApiView.as_view(), name="logoutUser"),

    path('register-user/', views.UserApiView.as_view(), name="userView"),
    path('register-user/<uuid:pk>/', views.UserDetailsApiView.as_view(), name="userDetails"),

    path('register-vendor/', views.VendorApiView.as_view(), name="vendorView"),
    path('register-vendor/<uuid:pk>/', views.VendorDetailsApiView.as_view(), name="vendorDetails"),

]
