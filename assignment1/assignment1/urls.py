"""
URL configuration for assignment1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('heritage_sites.urls')),  # Redirect to heritage_sites URLs for the homepage
    path('heritage_sites/', include('heritage_sites.urls')),  # Include URLs for heritage_sites
    path('', include('pwa.urls')),  # Include PWA URLs to manage service worker and manifest
    path('serviceworker.js', (TemplateView.as_view(template_name="serviceworker.js",
                                                   content_type='application/javascript', )),
         name='serviceworker.js'),
]
