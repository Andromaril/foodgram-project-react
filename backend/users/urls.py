from django.urls import include, path

from users.views import subscribe, subscriptions


urlpatterns_users_subscribe = [
    path('users/subscriptions/', subscriptions, name='subscriptions'),
    path('users/<int:following_id>/subscribe/', subscribe, name='subscribe'),
]

urlpatterns = [
    path('', include(urlpatterns_users_subscribe)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    
]