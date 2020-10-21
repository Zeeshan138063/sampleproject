from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView)

swaggerurls = [
    # OpenAPI sehema generation and swagger UI urls
    path('schema/',
         SpectacularAPIView.as_view(),
         name='schema'),
    # Optional UI swagger-UI:
    path('schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
]
