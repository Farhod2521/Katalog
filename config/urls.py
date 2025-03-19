"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from  .captcha import verify_captcha
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dj_rest_auth.views import LoginView
# from dj_rest_auth.views import PasswordResetConfirmView

schema_view = get_schema_view(
    openapi.Info(
        title = 'Elektron catalog',
        description = 'Qurilish resurslari milliy klassifikatori API',
        default_version = 'v1',
        terms_of_service = 'https://sarvarazim.uz/',
        contact = openapi.Contact(email='princeasia013@gmail.com', name='Prince Asia', url='https://tilshunos.com'),
        license = openapi.License(name='Hech qanaqa litsenziya'),
    ),
    public = True,
    permission_classes = (permissions.AllowAny, ),
    # docExpansion = 'none',
)

urlpatterns = [
    path('captcha/', include("captcha.urls")),
    path('api/captcha/', include("rest_captcha.urls")),
    path('dj-rest-auth/login/', LoginView.as_view(), name='rest_login'),
    # path('api/v1/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('api-auth/', include('rest_framework.urls')),
    # path('api/v1/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('rest-auth/password/reset/confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('api/allauth/', include('allauth.urls')),
    path('api/', include('users.urls')),
    path('materials/', include('app_materials.urls')),
    path('technos/', include('app_technos.urls')),
    # path('products/', include('app_products.urls')),
    path('machines-mechanos/', include('app_machines_and_mechanisms.urls')),
    path('small-mechanos/', include('app_small_mechanisms.urls')),
    path('works/', include('app_works.urls')),
    path('callback/', admin.site.urls),
    path('companies/', include('app_company.urls')),
    path('classifier/', include('app_csr.urls')),
    path('', include('app_api.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0,), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('order/', include('app_order.urls')),
    path('cmeta/', include('app_cmeta.urls')),
    path('api/verify-captcha/', verify_captcha, name='verify_captcha'),

]




if settings.DEBUG:   
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
