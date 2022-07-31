from .models import Notification
from .serializers import NotificationSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def list_user_notifications(request):
    id = request.user.id
    notifications = Notification.objects.filter(user__id=id)
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data)
