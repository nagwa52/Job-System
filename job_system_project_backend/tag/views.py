from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from tag.models import Tag
from tag.serializers import TagSerializer


@api_view(['GET'])
@authentication_classes([])
@permission_classes([IsAuthenticatedOrReadOnly])
def list_tags(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)

