from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


# user class master test wrapper to prevent nested test cases from running when other tests are running
class MasterTestWrapper:
    class MasterTest(APITestCase):
        endpoint = None
        methods = []
        kwargs = {}

        def get_url(self, *args, **kwargs):
            if not kwargs:
                kwargs = self.get_kwargs()
            return reverse(self.endpoint, args=args, kwargs=kwargs)

        def get_kwargs(self):
            return self.kwargs

        def authorize(self):
            self.refresh = RefreshToken.for_user(self.user)
            self.access_token = self.refresh.access_token
            self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        def setUp(self):
            self.user = User.objects.create_user(
                username='test_user',
                password='super_secure',
            )
            self.other_user = User.objects.create_user(
                username='other_user',
                password='super_secure',
            )

        def test_unauthorized_requests(self):
            url = self.get_url(**self.get_kwargs())
            for m in self.methods:
                try:
                    method = getattr(self.client, m.lower())
                    response = method(url)
                    if response:
                        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
                except AttributeError:
                    raise Exception(f"No such method {m}")
