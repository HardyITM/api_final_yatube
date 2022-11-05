from django.urls import path, include
from rest_framework.authtoken import views
from rest_framework import routers

from .views import PostViewSet, CommentViewSet, GroupViewSet, FollowViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'posts', PostViewSet)
router_v1.register(r'groups', GroupViewSet)
router_v1.register(r'follow', FollowViewSet, basename='follows')
router_v1.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments')

auth_patterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt'))
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
    path('v1/', include(auth_patterns))
]
