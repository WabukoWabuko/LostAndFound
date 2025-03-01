from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import Message
from django.contrib.auth.models import User
import jwt
from django.conf import settings

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.item_id = self.scope['url_route']['kwargs']['item_id']
        self.room_group_name = f'chat_{self.item_id}'
        
        # Extract token from query string
        token = self.scope['query_string'].decode().split('token=')[1] if 'token=' in self.scope['query_string'].decode() else None
        if token:
            try:
                # Decode JWT token (assuming HS256 and secret key in settings)
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                self.user = await User.objects.aget(id=payload['user_id'])
                self.scope['user'] = self.user
            except (jwt.InvalidTokenError, User.DoesNotExist):
                await self.close()
                return
        else:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        item_id = self.item_id

        try:
            item = await Item.objects.aget(id=item_id)
            receiver = await Item.objects.aget(id=item_id).created_by
            msg = await Message.objects.acreate(
                sender=self.scope['user'],
                receiver=receiver,
                item=item,
                content=message
            )
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': {
                        'id': msg.id,
                        'sender': {'id': self.scope['user'].id, 'username': self.scope['user'].username},
                        'receiver': {'id': receiver.id, 'username': receiver.username},
                        'item': item_id,
                        'content': message,
                        'timestamp': msg.timestamp.isoformat(),
                    }
                }
            )
        except Exception as e:
            print(f"Error saving message: {e}")

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
