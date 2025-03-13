from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.test import APITestCase
from watchlist_app.models import StreamPlatform, WatchList, Review


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="example")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.platform = StreamPlatform.objects.create(
            name="Netflix", about="#1 Platform", website="https://www.netflix.com"
        )

    def test_streamplatform_create(self):
        data = {
            "name": "Netflix",
            "about": "#1 Platform",
            "website": "https://www.netflix.com",
        }
        response = self.client.post(reverse("Stream-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse("Stream-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse("Stream-detail", args=(self.platform.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_streamplatform_update(self):
        data = {
            "name": "Netflix",
            "about": "#3 Platform",
            "website": "https://www.netflix.com",
        }
        response = self.client.put(
            reverse("Stream-detail", args=(self.platform.id,)), data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_streamplatform_delete(self):
        response = self.client.delete(
            reverse("Stream-detail", args=(self.platform.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class WatchListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="example", password="example")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.platform = StreamPlatform.objects.create(
            name="Netflix", about="#1 Platform", website="https://www.netflix.com"
        )

        self.watchlist = WatchList.objects.create(
            titile="Movie",
            description="Movie Storyline",
            platform=self.platform,
            active=True,
        )

    def test_watchlist_create(self):
        data = {
            "titile": "Example Movie",
            "description": "Example Movie Storyline",
            "platform": self.platform.id,
            "active": True,
        }
        response = self.client.post(reverse("WatchList-list"), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_watchlist_list(self):
        response = self.client.get(reverse("WatchList-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_watchlist_ind(self):
        response = self.client.get(reverse("WatchList-detail", args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(WatchList.objects.count(), 1)
        self.assertEqual(WatchList.objects.get().titile, "Movie")
        
    def test_watchlist_update(self):
        data = {
            "titile": "Example Movie",
            "description": "Example Movie Storyline",
            "platform": self.platform.id,
            "active": False,
        }
        response = self.client.put(reverse("WatchList-detail", args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_watchlist_delete(self):
        response = self.client.delete(reverse("WatchList-detail", args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)