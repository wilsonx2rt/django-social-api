from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from project.feed.models import Post

User = get_user_model()


class FeedDisplayTests(APITestCase):


    def setUp(self):
        user = get_user_model()
        super().setUp()
        for i in range(10):
            user = User.objects.create_user(
                username=f'user{i}',
                password='password'
            )
            Post.objects.create(
                user=user,
                content=f'Test post! {i}',
            )


    def test_post_feed_length(self):
        url = reverse('api:feed_display')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTIyMDE0MDgxLCJqdGkiOiJlOTkzYzYwMzVjODk0ZTMxODdiZmZiYzhhOWZiZjJiOSIsInVzZXJfaWQiOjJ9.WLXKyAMcdFl2mefYkfC6FFnXGYwC6oAcUPS5ES4eC0U')
        response = self.client.get(url, format="json")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 10)