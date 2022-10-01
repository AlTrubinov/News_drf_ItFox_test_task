from django.urls import path
from .views import NewsList, NewsDetail, CommentCreateView, CommentDetail

urlpatterns = [
    path('<int:news_pk>/comment/<int:pk>/', CommentDetail.as_view()),
    path('<int:news_pk>/comment/', CommentCreateView.as_view()),
    path('<int:pk>/', NewsDetail.as_view()),
    path('', NewsList.as_view()),

]
