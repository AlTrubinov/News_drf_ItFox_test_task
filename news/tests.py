from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import News, Comment
from .serializers import NewsSerializer


# class NewsTests(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Create a user
#         testuser1 = User.objects.create_user(username="testuser1", password="abc123")
#         testuser1.save()
#
#         # Create news
#         test_post = News.objects.create(
#             author=testuser1, title="News title", body="Body content..."
#         )
#         test_post.save()
#
#         # Create comment
#         test_comment = Comment.objects.create(
#             author=testuser1, news=News.objects.get(id=1), body="Comment body..."
#         )
#         test_comment.save()
#
#     def test_news_content(self):
#         news = News.objects.get(id=1)
#         author = f"{news.author}"
#         title = f"{news.title}"
#         body = f"{news.body}"
#         self.assertEqual(author, "testuser1")
#         self.assertEqual(title, "News title")
#         self.assertEqual(body, "Body content...")
#
#     def test_comment_content(self):
#         comment = Comment.objects.get(id=1)
#         author = f"{comment.author}"
#         news = f"{comment.news}"
#         body = f"{comment.body}"
#         self.assertEqual(author, "testuser1")
#         self.assertEqual(news, "News title")
#         self.assertEqual(body, "Comment body...")


class NewsTests(APITestCase):
    def setUp(self):
        # Create a user
        testuser1 = User.objects.create_user(username="testuser1", password="abc123")
        testuser1.save()

        # Create token for user
        self.testuser1_token = Token.objects.create(user=testuser1)

        # Create news
        self.test_post = News.objects.create(
            author=testuser1, title="News title", body="Body content..."
        )

        # Create comment
        self.test_comment = Comment.objects.create(
            author=testuser1, news=News.objects.get(id=1), body="Comment body..."
        )

    def test_newslist(self):
        response = self.client.get(reverse("news_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_news_detail(self):
        response = self.client.get(f"/api/v1/{self.test_post.pk}/")
        serializer_data = NewsSerializer(self.test_post).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)
