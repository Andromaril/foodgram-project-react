from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipes.urls'), name='recipe'),
    #path('api/', include('recipes.urls'), name='recipes'),
    path('', include('users.urls'), name='user'),
    #path('api/', include('users.urls'), name='users'),
    path(
    'redoc/',
    TemplateView.as_view(template_name='redoc.html'),
    name='redoc'),
]
