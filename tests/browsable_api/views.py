from __future__ import unicode_literals

from rest33 import authentication, renderers
from rest33.response import Response
from rest33.views import APIView


class MockView(APIView):

    authentication_classes = (authentication.SessionAuthentication,)
    renderer_classes = (renderers.BrowsableAPIRenderer,)

    def get(self, request):
        return Response({'a': 1, 'b': 2, 'c': 3})
