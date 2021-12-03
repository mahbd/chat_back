from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

from chat.permissions import CanUpdateChat

from .models import WSAuth, ChatRoom
from .serializers import ChatRoomSerializer, UserSerializer


def connection_test(request):
    return render(request, 'chat/connection_test.html')


class GetWSToken(APIView):
    def get(self, request: Request):
        if self.request.user.is_authenticated:
            auth_obj = WSAuth.objects.create(
                info=request._request.META['HTTP_USER_AGENT'], user=request.user)
            return Response({'ws_token': auth_obj.token})
        return Response({'result': 'User is not authenticated'}, status=401)


class ChatRoomViewSet(ModelViewSet):
    filter_backends = [SearchFilter, OrderingFilter]
    http_method_names = ['get', 'post', 'patch', 'delete']
    ordering_fields = ['chat_name', 'created_at', 'users__username', ]
    permission_classes = [IsAuthenticated, CanUpdateChat]
    queryset = ChatRoom.objects.all()
    search_fields = ['chat_name', 'users__username',
                     'users__first_name', 'users__last_name', 'users__email']
    serializer_class = ChatRoomSerializer


class UserViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['username', 'first_name', 'last_name', 'email']
    ordering_fields = ['username', 'first_name',
                       'last_name', 'email', 'last_login']
