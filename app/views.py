from typing import Dict

from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(('GET',))
def test_view(request: Dict) -> Response:
    return Response('Here I am!', 200)
