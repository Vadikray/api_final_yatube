import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from posts.models import Post, Group, Comment, Follow, User


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для постов."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для групп."""

    class Meta:
        model = Group
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок."""

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='username')

    class Meta:
        fields = '__all__'
        model = Follow
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=['user', 'following'],
            )
        ]

    def validate(self, data):
        """Проверка подписки на себя"""

        if self.context['request'].user == data['following']:
            raise serializers.ValidationError(
                'Нельзя подписываться на себя'
            )

        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""

    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('post',)
