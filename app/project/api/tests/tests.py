from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from project.api.tests.master_test import MasterTestWrapper
from project.feed.models import Post

User = get_user_model()


# simple test
# class FeedDisplayTests(APITestCase):
#
#     def setUp(self):
#         User = get_user_model()
#         super().setUp()
#         for i in range(10):
#             user = User.objects.create_user(
#                 username=f'user{i}',
#                 password='password'
#             )
#             Post.objects.create(
#                 user=user,
#                 content=f'Test post! {i}',
#             )
#
#     def test_post_feed_length(self):
#         url = reverse('api:feed_display')
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlI\
#         joiYWNjZXNzIiwiZXhwIjoxNTIyMDE0MDgxLCJqdGkiOiJlOTkzYzYwMzVjODk0ZTMxODdiZmZiYzhhOWZiZjJiOSIsInVzZXJfaWQiOjJ9.\
#         WLXKyAMcdFl2mefYkfC6FFnXGYwC6oAcUPS5ES4eC0U')
#         response = self.client.get(url, format="json")
#         self.assertEquals(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 10)


class FeedDisplayTests(MasterTestWrapper.MasterTest):
    endpoint = 'api:feed_display'
    methods = ['GET']

    def setUp(self):
        super().setUp()
        for i in range(10):
            Post.objects.create(
                user=self.user,
                content=f'Test post {i}',
            )
        self.url = self.get_url(**self.kwargs)

    def test_post_feed_length(self):
        self.authorize()
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data), 10)

    def test_post_feed_sort_descending_check(self):
        self.authorize()
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data[0].get('content'), 'Test post! 9')
