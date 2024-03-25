"""
URL configuration for icard project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include, re_path
from django.http import HttpResponse

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

#importaciones de rutas creadas en nuestro proyecto
from users.api.router import router_user

schema_view = get_schema_view(
   openapi.Info(
      title="API_BASE",
      default_version='v1',
      description="documentacion de la api",
      terms_of_service="https://pfr2102.github.io/PORTAFOLIO/",
      contact=openapi.Contact(email="pfrs2102@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


# Define la vista para la URL raíz
def index(request):
    return HttpResponse('''<h2> OK 200 </h2>
                        <h3> /admin --> panel de administración de django</h3> 
                        <h3> /docs --> documentación de la api <h3> 
                        <h3> /redoc --> documentación de la api redoc <h3>''', status=200)

urlpatterns = [
    #rutas globales de django
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #rutas de nuestras api
    path('', index),  # Ruta para la URL raíz
    path('api/', include(router_user.urls)),
    path('api/', include('users.api.router')),#esta ruta es diferente porque es para saber los datos del usuario que se autentica
]
