import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone

from chat.models import ChatRoom, ActiveChannel, WSAuth


class ChatConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = 'webSocket'

    async def connect(self):
        self.room_group_name = 'webSocket'
        self.scope['user'] = AnonymousUser()
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        event_type = text_data_json['type']
        if event_type == 'auth':
            user = await authenticate_user(text_data_json, self.channel_name)
            if isinstance(user, User):
                self.scope['user'] = user
                await self.send(text_data=json.dumps({
                    'type': 'auth',
                    'message': 'success'
                }))
            else:
                await self.send(text_data=json.dumps({
                    'type': 'auth',
                    'message': user
                }))
        elif event_type == 'message':
            response = await handle_message(text_data_json, self.scope['user'])
            if response:
                self.channel_layer.send(
                    self.channel_name,
                    {
                        "type": "chat_message",
                        "event": "failed_message",
                        "message": text_data_json.get('message'),
                        "chat_id": text_data_json.get('chat_id'),
                        "error_message": response
                    }
                )

    # Receive message from room group
    async def send_data(self, event):
        message = event['data']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'data': message
        }))

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))


@database_sync_to_async
def handle_message(event_obj: dict, user=None) -> None | str:
    if not user.is_authenticated:
        return "User is not authenticated"
    message = event_obj.get('message')
    chat_id = event_obj.get('chat_id')
    if not message:
        return "Message is empty"
    if not chat_id:
        return "Chat id is empty"
    try:
        chat_info = ChatRoom.objects.get(id=chat_id)
    except ChatRoom.DoesNotExist:
        return "Chat doesn't exist"
    chat_users = chat_info.users.all()
    if user not in chat_users:
        return "User is not in chat"
    for user in chat_users:
        user: User = user
        channel_layer = get_channel_layer()
        for active_channel in user.activechannel_set.all():
            async_to_sync(channel_layer.send)(active_channel.channel, {
                'type': 'chat_message',
                'message': message,
                'chat_id': chat_id,
                'user': user.id,
            })
    return None


@database_sync_to_async
def authenticate_user(event_obj: dict, channel_name: str) -> User | str:
    ws_token = event_obj.get('ws_token')
    if not WSAuth.objects.filter(token=ws_token).exists():
        return "Invalid ws token"
    ws_auth_obj = WSAuth.objects.get(token=ws_token)
    if ws_auth_obj.valid_till < timezone.now():
        return "Token validity expired"
    ActiveChannel.objects.create(
        channel=channel_name, info=ws_auth_obj.info, user=ws_auth_obj.user)
    return ws_auth_obj.user
