from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('chat-room', views.ChatRoomViewSet, basename='chat-room')
router.register('users', views.UserViewSet, basename='users')


urlpatterns = [
    path('connection-test/', views.connection_test, name='connection-test'),
    path('get-ws-token/', views.GetWSToken.as_view(), name='get-ws-token'),
    path('', include(router.urls)),
]
