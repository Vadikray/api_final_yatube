from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import IsOwnerOrReadOnly
from .serializers import (PostSerializer,
                          GroupSerializer,
                          CommentSerializer,
                          FollowSerializer
                          )
from posts.models import Post, Group, User


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для постов."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Создания поста."""

        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет для групп."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsOwnerOrReadOnly]


class FollowViewSet(viewsets.ModelViewSet):
    """Вьюсет для подписок."""

    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.SearchFilter, )
    search_fields = ('following__username', )

    def get_queryset(self):
        """Определения подписок"""

        following = get_object_or_404(
            User, username=self.request.user.username)

        return following.follower

    def perform_create(self, serializer):
        """Cоздания подписки"""

        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""

    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        """Определения комментариев."""

        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))

        return post.comments.all()

    def perform_create(self, serializer):
        """Cоздания комментария."""

        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)
