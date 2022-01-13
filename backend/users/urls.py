from users.views import FollowViewSet
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),
]