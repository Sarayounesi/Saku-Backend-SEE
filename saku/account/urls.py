from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import Register, CompeleteRegisteration, ChangePassword, ForgotPassword

app_name = "account"
urlpatterns = [
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='login'),
    path("logout/", jwt_views.TokenRefreshView.as_view(), name="logout"),
    path("verify/", jwt_views.TokenVerifyView.as_view(), name="verify"),
    path("register/", Register.as_view(), name="register"),
    path("register/verify/", CompeleteRegisteration.as_view(), name="register_verify"),
    path("change_password/", ChangePassword.as_view(), name="change_password"),
    path("forgot_password/", ForgotPassword.as_view(), name="forgot_password"),
]