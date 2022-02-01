from django.urls import include, path

from users.views import subscribe, subscriptions

urlpatterns = [
    path('users/<int:following_id>/subscribe/', subscribe,
         name='subscribe'),
    path('users/subscriptions/', subscriptions,
         name='subscription'),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

]
