from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import subscribe, subscriptions

app_name = 'api'

urlpatterns_users_subscribe = [
    path('users/subscriptions/', subscriptions, name='subscriptions'),
    path('users/<int:following_id>/subscribe/', subscribe, name='subscribe'),
]

urlpatterns = [
    path('', include(urlpatterns_users_subscribe)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    
]