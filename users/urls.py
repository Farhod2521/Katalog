from django.urls import path

from .views import (
    LoginByDigitalSignatureView,
    UserDSView,
    # RegisterView,
    LoginView,
    UserView,
    LogoutView,
    # SetUserCompanyView,
    # UserUpdateAPIView,
    UserAdsStatView,
    UserTopAdsView,
    RegisterAPIView,
    password_change_view,
    VerifyEmailAPIView, 
    ResendVerificationCodeAPIView,
    PasswordResetRequestAPIView,
    PasswordResetConfirmAPIView,
    PasswordResetCodeAPIView, 
    OneIDLoginView
    
    )

urlpatterns = [
    path('login', LoginView.as_view()),
    path('oneid-login', OneIDLoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('customer/', UserView.as_view()),
    # path('user/update', UserUpdateAPIView.as_view()),
    
    # path('set/company', SetUserCompanyView.as_view()),
    path('user', UserDSView.as_view()),
    path('user/stat', UserAdsStatView.as_view()),
    path('user/top', UserTopAdsView.as_view()),
    path('imzo', LoginByDigitalSignatureView.as_view()),

    path('cutomer/register/', RegisterAPIView.as_view()),
    path('passowrd/change/', password_change_view, name="password-change"),
    path('verify-email/', VerifyEmailAPIView.as_view(), name='verify-email'),
    path('resend-verification-code/', ResendVerificationCodeAPIView.as_view(), name='resend-verification-code'),
    path('password_reset/', PasswordResetRequestAPIView.as_view(), name='password_reset_request'),
    path('password_reset/confirm_code/', PasswordResetCodeAPIView.as_view(), name='password_reset_confirm_code'),
    path('password_reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'),


]
