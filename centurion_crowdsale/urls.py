from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from centurion_crowdsale.invest_requests.views import InvestRequestView, ValidateUsdAmountView
from centurion_crowdsale.vouchers.views import VoucherActivationView
from centurion_crowdsale.projects.views import CenturionProjectViewSet
from centurion_crowdsale.rates.views import UsdRateView
from centurion_crowdsale.quantum.views import create_charge, change_charge_status
from rest_framework.routers import DefaultRouter

schema_view = get_schema_view(
    openapi.Info(
        title="Centurion Crowdsale API",
        default_version='v1',
        description="API for centurion crowdsale backend",
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter(trailing_slash=True)
router.register('projects', CenturionProjectViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/', include(router.urls)),
    # path('api/v1/swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/v1/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/activate_voucher', VoucherActivationView.as_view()),
    path('api/v1/usd_rates/', UsdRateView.as_view()),
    path('api/v1/projects/<str:string_id>/invest', InvestRequestView.as_view()),
    path('api/v1/projects/<str:string_id>/validate_usd_amount', ValidateUsdAmountView.as_view()),
    path('api/v1/projects/<str:string_id>/create_charge', create_charge),
    path('api/v1/change_charge_status/', change_charge_status),
]
