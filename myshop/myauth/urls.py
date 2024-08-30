from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import hello, RegisterView, LogoutView

from django.urls import path


app_name = 'myauth'

urlpatterns = [
    path('', hello, name='hello'),
    path('login/', TokenObtainPairView.as_view(), name='token-login'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]