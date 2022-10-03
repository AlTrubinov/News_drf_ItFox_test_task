from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import NewsList, NewsDetail, CommentCreateView, CommentDetail

router = DefaultRouter()
router.register(r"", NewsDetail)

urlpatterns = [
    path("<int:news_pk>/comment/<int:pk>/", CommentDetail.as_view()),
    path("<int:news_pk>/comment/", CommentCreateView.as_view()),
    path("", NewsList.as_view()),
] + router.urls
