from rest_framework import viewsets, permissions, filters, mixins
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.viewsets import GenericViewSet

from .permissions import AuthorOrReadOnly, ReadOnly
from posts.models import Post, Comment, Group, Follow
from .serializers import (
    CommentSerializer,
    PostSerializer,
    GroupSerializer,
    FollowSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (AuthorOrReadOnly, )

    def perform_create(self, serializer): 
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrReadOnly,)

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        new_queryset = Comment.objects.filter(post=post_id)
        return new_queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class GetAndPostViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    GenericViewSet):
    pass


class FollowViewSet(GetAndPostViewSet):
    serializer_class = FollowSerializer
    queryset = Follow.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username', 'user__username')

    def get_queryset(self):
        user = self.request.user.author.all()
        return user

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
