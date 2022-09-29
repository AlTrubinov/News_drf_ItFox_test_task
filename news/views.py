from rest_framework import generics
from .models import News
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import NewsSerializer


class NewsList(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    queryset = News.objects.all()
    serializer_class = NewsSerializer
