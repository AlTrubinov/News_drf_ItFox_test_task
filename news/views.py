from rest_framework import generics
from rest_framework import viewsets

from .mixins import LikedMixin
from .models import News, Comment
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import NewsSerializer, CommentSerializer


class NewsList(generics.ListCreateAPIView):
    queryset = News.objects.order_by('-created_at')
    serializer_class = NewsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsDetail(LikedMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class CommentCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        news = self.kwargs['news_pk']
        return Comment.objects.filter(news_id=news)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, news_id=self.kwargs['news_pk'])


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
