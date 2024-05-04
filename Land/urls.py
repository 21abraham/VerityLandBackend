from django.urls import path
from .views import UserRegistrationAPIView,LoginAPIView,LogoutAPIView,refresh_token,TokenVerificationAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('refresh_token/', refresh_token, name='refresh_token'),
    path('token-verify/', TokenVerificationAPIView.as_view(), name='token_verify'),
]
