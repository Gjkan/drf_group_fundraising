from django.urls import path
from .views import *
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny, ],
)


urlpatterns = [
                path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
                path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
                path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
                path('', ApiOverview, name='home'),
                path('collects/create/', CollectCreate.as_view(), name='collect-create-api-view'),
                path('collects/', CollectDetail.as_view(), name='collects-detail-api-view'),
                path('collects/<int:pk>/', CollectDetail.as_view(), name='collect-detail-api-view'),
                path('collects/<int:pk>/update/', CollectUpdate.as_view(), name='collect-update-api-view'),
                path('collects/<int:pk>/delete/', CollectDelete.as_view(), name='collect-delete-api-view'),
                path('payments/create/', PaymentCreate.as_view(), name='payment-create-api-view'),
                path('payments/', PaymentDetail.as_view(), name='payments-detail-api-view'),
                path('payments/<int:pk>/', PaymentDetail.as_view(), name='payment-detail-api-view'),
                path('payments/<int:pk>/update/', PaymentUpdate.as_view(), name='payment-update-api-view'),
                path('payments/<int:pk>/delete/', PaymentDelete.as_view(), name='payment-delete-api-view'),
]
