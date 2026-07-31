from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny

from .models import CustomUser, Event
from .serializers import UserSerializer, EventSerializer

class UserListCreateView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAdminUser()]
        return [AllowAny()]

    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventListView(APIView):
    permission_classes = [AllowAny]

    @method_decorator(cache_page(60 * 5)) # Кэш 5 минут
    def get(self, request):
        now = timezone.now()
        events = Event.objects.filter(meeting_time__gt=now)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

class EventSubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        now = timezone.now()
        try:
            event = Event.objects.get(pk=pk, meeting_time__gt=now)
        except Event.DoesNotExist:
            return Response(
                {"detail": "Событие не найдено или уже началось."},
                status=status.HTTP_404_NOT_FOUND
            )

        event.users.add(request.user)
        return Response(
            {"detail": f"Вы успешно подписались на '{event.name}'"},
            status=status.HTTP_200_OK
        )

class MyEventsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        events = request.user.events.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)