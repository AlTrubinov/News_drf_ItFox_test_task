from rest_framework import serializers
from .models import News, Comment


class LimitedListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.order_by('-created_at')[:10]
        return super().to_representation(data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    news = serializers.ReadOnlyField(source='news.title')

    class Meta:
        model = Comment
        fields = ('id', 'news', 'author', 'body', 'created_at',)


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True)

    class Meta:
        model = News
        fields = ('id', 'author', 'title', 'body', 'comments', 'created_at',)
