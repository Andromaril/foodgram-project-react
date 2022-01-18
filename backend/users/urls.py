from users.views import FollowViewSet, UserViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
#router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),

    #path('api/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]