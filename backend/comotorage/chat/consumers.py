import json
import re
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from .models import Message
from asgiref.sync import sync_to_async
import urllib.parse

User = get_user_model()

def safe_group_name(name):
    # Remplace tout caractère non autorisé par un underscore
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', name)

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        user1 = self.scope['user'].email
        user2 = urllib.parse.unquote(self.room_name)
        # Encode les deux usernames pour le nom du groupe
        safe_user1 = safe_group_name(user1)
        safe_user2 = safe_group_name(user2)
        self.room_group_name = f"chat_{'_'.join(sorted([safe_user1, safe_user2]))}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({"error": "Invalid JSON"}))
            return
    
        sender = self.scope['user']
        if not sender.is_authenticated:
            await self.send(text_data=json.dumps({"error": "User not authenticated"}))
            return
    
        receiver = await self.get_receiver_user()
        if receiver is None:
            await self.send(text_data=json.dumps({"error": "Receiver does not exist"}))
            return
    
        msg = await self.save_message(sender, receiver, text_data_json['message'])
    
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender.email,
                'receiver': receiver.email,
                'message': msg.content,
                'timestamp': msg.timestamp.strftime('%d/%m/%Y %H:%M')
            }
        )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'sender': event['sender'],
            'receiver': event['receiver'],
            'message': event['message'],
            'timestamp': event['timestamp']
        }))

   
    @sync_to_async
    def save_message(self, sender, receiver, message):
        return Message.objects.create(sender=sender, receiver=receiver, content=message)

    @sync_to_async
    def get_receiver_user(self):
        decoded_email = urllib.parse.unquote(self.room_name)
        try:
            return User.objects.get(email=decoded_email)
        except User.DoesNotExist:
            return None