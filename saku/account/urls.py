from django.urls import path
from rest_framework_simplejwt import views as jwt_views

app_name = "account"
urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path("logout/", jwt_views.TokenRefreshView.as_view(), name="logout"),
    path("verify/", jwt_views.TokenVerifyView.as_view(), name="verify"),
]