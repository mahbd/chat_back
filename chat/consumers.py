import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser


# noinspection PyAttributeOutsideInit
class ChatConsumer(AsyncWebsocketConsumer):
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
        message = text_data_json['message']
        if text_data_json.get('user'):
            user = text_data_json['user'][:3]
        else:
            user = 'Unk'
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user
            }
        )

    # Receive message from room group
    async def send_data(self, event):
        message = event['data']
        print(message)
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'data': message
        }))

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))
