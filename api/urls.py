from django.conf.urls import include
from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView, SpectacularSwaggerView)

urlpatterns = [
    path("users/", include("api.users.urls")),
    #OpenAPI sehema generation and swagger UI urls
    path('api/schema/',
         SpectacularAPIView.as_view(),
         name='schema'),
    # Optional UI:
    path('api/schema/swagger-ui/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
]
