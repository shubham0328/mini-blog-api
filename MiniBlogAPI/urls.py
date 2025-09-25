

#Required so that HTTP requests like /api/posts/ reach your views.py.

"""
URL configuration for MiniBlogAPI project.
"""

from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

def api_root(request):
    return JsonResponse({
        "message": "Welcome to Mini Blog API",
        "endpoints": [
            "/api/token/",               # Get access & refresh token
            "/api/token/refresh/",       # Refresh access token
            "/api/posts/",
            "/api/posts/<id>/",
            "/api/posts/<id>/comments/"
        ]
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # JWT authentication endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # API root + blog app endpoints
    path("api/", api_root),
    path("api/", include("blog.urls")),
]
