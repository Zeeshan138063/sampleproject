from django.conf.urls import include
from django.urls import path

from api.swaggerurls import swaggerurls

urlpatterns = [
    path("users/", include("api.users.urls")),
]

urlpatterns += swaggerurls
