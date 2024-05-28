from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.urls import path
from django.conf.urls import url

schema_view = get_schema_view(
    openapi.Info(
        title="config main API Documentation",
        default_version='v1',
        description="Documentation for your API",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

urlpatterns = [
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
