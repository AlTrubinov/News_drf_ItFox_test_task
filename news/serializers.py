from rest_framework import serializers
from .models import News, Comment
from . import services


class LimitedListSerializer(serializers.ListSerializer):
    """Sorting query by created time and limited to 10 entries"""

    def to_representation(self, data):
        try:
            data = data.order_by("-created_at")[:10]
        finally:
            return super().to_representation(data)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    news = serializers.ReadOnlyField(source="news.title")

    class Meta:
        list_serializer_class = LimitedListSerializer
        model = Comment
        fields = (
            "id",
            "news",
            "author",
            "body",
            "created_at",
        )


class NewsSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    comments = CommentSerializer(many=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = News
        fields = (
            "id",
            "author",
            "title",
            "body",
            "is_liked",
            "total_likes",
            "total_comments",
            "comments",
            "created_at",
        )

    def get_is_liked(self, obj) -> bool:
        """Checks if the user liked the news"""

        user = self.context.get("request").user
        return services.is_liked(obj, user)
