
from django.conf.urls import url
from django.contrib.auth.models import User

from rest33.authentication import TokenAuthentication
from rest33.authtoken.models import Token
from rest33.test import APITestCase
from rest33.views import APIView

urlpatterns = [
    url(r'^$', APIView.as_view(authentication_classes=(TokenAuthentication,))),
]


class MyMiddleware(object):

    def process_response(self, request, response):
        assert hasattr(request, 'user'), '`user` is not set on request'
        assert request.user.is_authenticated(), '`user` is not authenticated'
        return response


class TestMiddleware(APITestCase):

    urls = 'tests.test_middleware'

    def test_middleware_can_access_user_when_processing_response(self):
        user = User.objects.create_user('john', 'john@example.com', 'password')
        key = 'abcd1234'
        Token.objects.create(key=key, user=user)

        with self.settings(
            MIDDLEWARE_CLASSES=('tests.test_middleware.MyMiddleware',)
        ):
            auth = 'Token ' + key
            self.client.get('/', HTTP_AUTHORIZATION=auth)
