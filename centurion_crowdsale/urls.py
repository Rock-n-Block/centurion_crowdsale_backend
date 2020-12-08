"""centurion_crowdsale URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from centurion_crowdsale.invest_requests.views import InvestRequestView, ValidateUsdFromDucAmountView
from centurion_crowdsale.vouchers.views import VoucherActivationView
from centurion_crowdsale.projects.views import CenturionProjectView, CenturionProjectsView
from centurion_crowdsale.rates.views import UsdRateView

schema_view = get_schema_view(
    openapi.Info(
        title="Ducatus Crowdsale API",
        default_version='v1',
        description="API for ducatus crowdsale backend",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('api/v1/swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/activate_voucher/', VoucherActivationView.as_view()),
    path('api/v1/usd_rates/', UsdRateView.as_view()),
    path('api/v1/projects/<int:id>/invest', InvestRequestView.as_view()),
    path('api/v1/projects/<int:id>/validate_usd_from_duc', ValidateUsdFromDucAmountView.as_view()),
    path('api/v1/projects/<int:id>/', CenturionProjectView.as_view()),
    path('api/v1/projects/', CenturionProjectsView.as_view()),
]
