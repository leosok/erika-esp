"""
URL configuration for erika_cloud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from ninja import NinjaAPI

from frontend.views import index
from typewriter.api import typewriter_router
from typewriter.views import user_dashboard
from .api import router as erika_cloud_api

api = NinjaAPI()

# Optionally, you can add routes here if you have additional routes directly in this file
# Example: api.add_router("/somepath", some_module.router)

# Include typewriter API
api.add_router("/typewriter", typewriter_router)
api.add_router("/erika_cloud", erika_cloud_api)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path('accounts/', include('allauth.urls')), # new
    path('dashboard/', user_dashboard, name='user_dashboard'),
    path('', index, name='frontend_index'),

]
