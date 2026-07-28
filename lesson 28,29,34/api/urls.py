from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    UserListCreateView,
    EventListView,
    EventSubscribeView,
    MyEventsView
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListCreateView.as_view(), name='user-list-create'),

    # Новые эндпоинты для работы с событиями:
    path('events/', EventListView.as_view(), name='event-list'),
    path('event/<int:pk>/', EventSubscribeView.as_view(), name='event-subscribe'),
    path('events/my/', MyEventsView.as_view(), name='my-events'),
]