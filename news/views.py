from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet

from .mixins import LikedMixin
from .models import News, Comment
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import NewsSerializer, CommentSerializer


class NewsList(ListCreateAPIView):
    queryset = News.objects.order_by("-created_at")
    serializer_class = NewsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsDetail(LikedMixin, ModelViewSet):
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CommentCreateView(ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        news = self.kwargs["news_pk"]
        return Comment.objects.filter(news_id=news)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, news_id=self.kwargs["news_pk"])


class CommentDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
