import base64
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from search_app.models import WikiSearchLog


class WordFrequencyViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        credentials = f"{self.user.username}:testpassword"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {encoded_credentials}")

    def test_word_frequency_view_success(self):
        data = {"title": "Python", "num_words": 5}
        url = reverse("search-view")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("most_common_words", response.data)

    def test_word_frequency_view_missing_data(self):
        data = {"title": "Python"}  # num_words is missing
        url = reverse("search-view")  # Assuming 'search-view' is the name of the URL
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)


class SearchHistoryLogTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username="adminuser", password="adminpassword", email="admin@example.com"
        )

        self.normal_user = User.objects.create_user(
            username="otheruser", password="otherpassword"
        )
        self.log_entry = WikiSearchLog.objects.create(
            user=self.admin_user,
            article="Python",
            word_count=5,
            word_frequency={"Python": 5},
        )

    def set_admin_credentials(self):
        encoded_credentials = self.encode_credentials(
            self.admin_user.username, "adminpassword"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {encoded_credentials}")

    def set_normal_user_credentials(self):
        encoded_credentials = self.encode_credentials(
            self.normal_user.username, "otherpassword"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Basic {encoded_credentials}")

    def encode_credentials(self, username, password):
        credentials = f"{username}:{password}"
        return base64.b64encode(credentials.encode()).decode()

    def test_search_history_log_superuser(self):
        self.set_admin_credentials()
        url = reverse("search-log")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_search_history_log_regular_user(self):
        self.set_normal_user_credentials()
        url = reverse("search-log")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_search_history_log_unauthenticated(self):
        self.client.credentials()
        url = reverse("search-log")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
