from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import (
    APITestCase,
    APIRequestFactory,
    APIClient,
)
from django.contrib.auth.models import User
from .models import News, Comment
from .serializers import NewsSerializer, CommentSerializer


class NewsTests(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        # Create a user1
        self.testuser1 = User.objects.create_user(
            username="testuser1", password="abc123"
        )
        self.testuser1.save()

        # Create a user2
        self.testuser2 = User.objects.create_user(
            username="testuser2", password="abc123"
        )
        self.testuser2.save()

        # Create token for users
        self.testuser1_token = Token.objects.create(user=self.testuser1)
        self.testuser1_token.save()

        # Create news
        self.test_post = News.objects.create(
            author=self.testuser1, title="Test title", body="Test content..."
        )
        self.test_post.save()

        # Create comment
        self.test_comment = Comment.objects.create(
            author=self.testuser1, news=self.test_post, body="Comment test"
        )
        self.test_comment.save()

        self.client = APIClient()

    def test_news_list(self):
        response = self.client.get(reverse("news_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_news_detail(self):
        response = self.client.get(f"/api/v1/{self.test_post.pk}/")
        serializer_data = NewsSerializer(self.test_post).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_invalid_news_update(self):
        response = self.client.put(
            f"/api/v1/{self.test_post.pk}/",
            {
                "title": "News title",
                "body": "Body content...(update)",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_authorized_news_update(self):
        self.client.login(username=self.testuser2.username, password="abc123")
        response = self.client.put(
            f"/api/v1/{self.test_post.pk}/",
            {
                "title": "News title",
                "body": "Body content...(update)",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_news_update(self):
        self.client.login(username=self.testuser1.username, password="abc123")
        response = self.client.put(
            f"/api/v1/{self.test_post.pk}/",
            {
                "title": "News title",
                "body": "Body content...(update)",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_news_delete(self):
        response = self.client.delete(f"/api/v1/{self.test_post.pk}/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_authorized_news_delete(self):
        self.client.login(username=self.testuser2.username, password="abc123")
        response = self.client.delete(f"/api/v1/{self.test_post.pk}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_news_delete(self):
        self.client.login(username=self.testuser1.username, password="abc123")
        response = self.client.delete(f"/api/v1/{self.test_post.pk}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_news_create(self):
        response = self.client.post(
            "/api/v1/",
            {
                "title": "News title",
                "body": "Body content...",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_news_create(self):
        self.client.login(username=self.testuser1.username, password="abc123")
        response = self.client.post(
            "/api/v1/",
            {
                "title": "News title",
                "body": "Body content...",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_news_comments(self):
        response = self.client.get(
            reverse("news_comments_list", kwargs={"news_pk": self.test_post.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_news_comments_detail(self):
        response = self.client.get(
            reverse(
                "news_comment_detail",
                kwargs={
                    "news_pk": self.test_post.pk,
                    "pk": self.test_comment.pk,
                },
            )
        )
        serializer_data = CommentSerializer(self.test_comment).data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)

    def test_invalid_comment_create(self):
        response = self.client.post(
            reverse("news_comments_list", kwargs={"news_pk": self.test_post.pk}),
            {
                "body": "Test comment content...",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_comment_create(self):
        self.client.login(username=self.testuser1.username, password="abc123")
        response = self.client.post(
            reverse("news_comments_list", kwargs={"news_pk": self.test_post.pk}),
            {
                "body": "Test comment content...",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_comment_update(self):
        response = self.client.put(
            reverse(
                "news_comment_detail",
                kwargs={
                    "news_pk": self.test_post.pk,
                    "pk": self.test_comment.pk,
                },
            ),
            {
                "body": "Updated test comment content...",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_authorized_comment_update(self):
        self.client.login(username=self.testuser2.username, password="abc123")
        response = self.client.put(
            reverse(
                "news_comment_detail",
                kwargs={
                    "news_pk": self.test_post.pk,
                    "pk": self.test_comment.pk,
                },
            ),
            {
                "body": "Updated test comment content...",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authorized_comment_update(self):
        self.client.login(username=self.testuser1.username, password="abc123")
        response = self.client.put(
            reverse(
                "news_comment_detail",
                kwargs={
                    "news_pk": self.test_post.pk,
                    "pk": self.test_comment.pk,
                },
            ),
            {
                "body": "Updated test comment content...",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_like_news(self):
        response = self.client.get(f"/api/v1/{self.test_post.pk}/like/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_unlike_news(self):
        response = self.client.get(f"/api/v1/{self.test_post.pk}/unlike/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_like_news(self):
        self.client.login(username=self.testuser1.username, password="abc123")
        response = self.client.get(f"/api/v1/{self.test_post.pk}/like/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unlike_news(self):
        self.client.login(username=self.testuser1.username, password="abc123")
        response = self.client.get(f"/api/v1/{self.test_post.pk}/unlike/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_token_create(self):
        response = self.client.post("/auth/token/login", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_create(self):
        response = self.client.post(
            "/auth/token/login",
            {"password": "abc123", "username": self.testuser1.username},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_authorized_news_create(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.testuser1_token.key)
        response = self.client.post(
            "/api/v1/",
            {
                "title": "News title",
                "body": "Body content...",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
