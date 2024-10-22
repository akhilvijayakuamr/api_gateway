import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from .service import *
from channels.db import database_sync_to_async
import ast
from userservice.service import APIUserClient

userclient = APIUserClient()

# Chat consumer


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode() 
        query_params = parse_qs(query_string)  
        chat_user_id = query_params.get('chat_user', [None])[0]
        user_id = query_params.get('user', [None])[0]
        user_ids = [int(user_id), int(chat_user_id)]
        user_ids = sorted(user_ids)
        self.room_group_name = f"chat_{user_ids[0]}-{user_ids[1]}"
        await self.get_or_create_chat_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        
        
    @database_sync_to_async
    def get_or_create_chat_room(self):
        query_string = self.scope['query_string'].decode() 
        query_params = parse_qs(query_string)  
        chat_user_id = query_params.get('chat_user', [None])[0]
        user_id = query_params.get('user', [None])[0]
        response = crete_room(user_id, chat_user_id)
        return response
        

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', '')
        
        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
            }
        )
        
        
    @database_sync_to_async
    def save_message(self, message):
        query_string = self.scope['query_string'].decode() 
        query_params = parse_qs(query_string)  
        chat_user_id = query_params.get('chat_user', [None])[0]
        user_id = query_params.get('user', [None])[0]
        response = message_save(user_id, chat_user_id, message)
        return response
    
    
    @database_sync_to_async
    def get_message_object(self, message_content):
        message = message_obj(message_content)
        decoded_message = message.decode('utf-8')

        message_dict = ast.literal_eval(decoded_message)
        return {
            'id': message_dict['id'],
            'chat_room': message_dict['chat_room'],
            'user': message_dict['user'],
            'content': message_dict['content'],
            'timestamp': message_dict['timestamp']
        }
        
    
    async def chat_message(self, event):
        message = event['message']
        message_obj = await self.get_message_object(message)
        print(message_obj)
        await self.send(text_data=json.dumps(message_obj))




# Notification Consumer


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode() 
        query_params = parse_qs(query_string) 
        user_id = query_params.get('user', [None])[0]
        user_ids = int(user_id)
        self.room_group_name = f"notification_{user_ids}"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.set_user_online(user_ids)


    async def disconnect(self, close_code):
        query_string = self.scope['query_string'].decode() 
        query_params = parse_qs(query_string) 
        user_id = query_params.get('user', [None])[0]
        user_ids = int(user_id)
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.set_user_offline(user_ids)

    

    @database_sync_to_async
    def get_notification_object(self, notification_content):
        notification = notification_obj(notification_content)
        decoded_notification = notification.decode('utf-8')

        notification_dict = ast.literal_eval(decoded_notification)
        profile_response =  userclient.post_unique_data(notification_dict['another_user'])


        return {
            'another_user':notification_dict['another_user'],
            'content': notification_dict['content'],
            'follower':notification_dict['follower'],
            'full_name':profile_response.full_name,
            'id':notification_dict['id'],
            'post':notification_dict['post'],
            'read':notification_dict['read'],
            'timestamp':notification_dict['timestamp'],
            'user_profile':profile_response.profile_image
        }
        
    
    async def send_notification(self, event):
        notification = event['notification']
        notification_obj = await self.get_notification_object(notification)
        await self.send(text_data=json.dumps(notification_obj))



    @database_sync_to_async
    def set_user_online(self, user_id):
        res = user_online(user_id)
        print(res)

    @database_sync_to_async
    def set_user_offline(self, user_id):
        res = user_offline(user_id)
        print(res)