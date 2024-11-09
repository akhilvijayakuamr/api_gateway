from django.http import JsonResponse
from .rabbitmq import RpcClient
from api_gateway.auth import authorization
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import ast





# Create Room

def crete_room(user_id, chat_user_id):
    sender_id = user_id
    receiver_id = chat_user_id
    opration = "create_room"
        
    payload = {
                'sender_id':sender_id,
                'receiver_id':receiver_id,
                'opration':opration}
        
    client = RpcClient()
    response = client.call(payload)  
    return response


# Message save


def message_save(user_id, chat_user_id, message):
    sender_id = user_id
    receiver_id = chat_user_id
    message_content = message
    opration = "save_message"
    
    payload = {
                'sender_id':sender_id,
                'receiver_id':receiver_id,
                'message_content':message_content,
                'opration':opration}
    
        
    client = RpcClient()
    response = client.call(payload)
    decoded_string = response.decode('utf-8')
    data_list = ast.literal_eval(decoded_string)
    print("responses get", data_list)
    if(data_list):
        message_triger(receiver_id, data_list)
    return data_list
    



    
# Message object

def message_obj(message_content):
    message_content = message_content
    opration = "get_message"
    
    payload = {
        'message_content':message_content,
        'opration':opration
    }
    
    client = RpcClient()
    response = client.call(payload)
    return response



# Get specific user chat


def chat_list(sender_id, receiver_id):

    opration = "get_all_chat"

    payload = {
            'sender_id':sender_id,
            'receiver_id':receiver_id,
            'opration':opration
                }
                
    client = RpcClient()
    response = client.call(payload)
    return response



# Get all user chat

def all_chat_user(user_id):

    opration = "all_chat_user"

    payload = {
        'user_id':user_id,
        'opration':opration
    }

    client = RpcClient()
    response = client.call(payload)
    return response



# Notification for followers

def follow_notification(user_id, another_user_id):
    opration = "follow_notification"

    payload = {
        'user_id':user_id,
        'another_user_id':another_user_id,
        'opration':opration
    }
    client = RpcClient()
    response = client.call(payload)
    decoded_string = response.decode('utf-8')
    data_list = ast.literal_eval(decoded_string)
    id = data_list[0]
    content = data_list[1]
    send_notification_to_group(id,content)
    return response



# Notification for like


def like_notification(user_id, another_user_id, post_id):
    opration = "like_notification"
    payload = {
        'user_id':user_id,
        'another_user_id':another_user_id,
        'post_id':post_id,
        'opration':opration
    }
    client = RpcClient()
    response = client.call(payload)
    decoded_string = response.decode('utf-8')
    data_list = ast.literal_eval(decoded_string)
    id = data_list[0]
    content = data_list[1]
    send_notification_to_group(id,content)
    return response


# Notification for comment

def comment_notification(user_id, another_user_id, post_id):
    opration = "comment_notification"
    payload = {
        'user_id':user_id,
        'another_user_id':another_user_id,
        'post_id':post_id,
        'opration':opration
    }
    client = RpcClient()
    response = client.call(payload)
    decoded_string = response.decode('utf-8')
    data_list = ast.literal_eval(decoded_string)
    id = data_list[0]
    content = data_list[1]
    send_notification_to_group(id,content)
    return response



# Get all notifications

def get_all_notification(user_id):

    opration = "all_notification"

    payload = {
        'user_id':user_id,
        'opration':opration
    }

    client = RpcClient()
    response = client.call(payload)
    return response




# Read notifications

def read_all_notification(user_id):

    opration = "read_notification"

    payload = {
        'user_id':user_id,
        'opration':opration
    }

    client = RpcClient()
    response = client.call(payload)
    return response




# Notifiation object

def notification_obj(notification_content):
    notification_content = notification_content
    opration = "get_notification"
    
    payload = {
        'notification_content':notification_content,
        'opration':opration
    }
    
    client = RpcClient()
    response = client.call(payload)
    return response




# send notification

def send_notification_to_group(id, notification):
    group_name = f"notification_{id}"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_notification',
            'notification': notification,
        }
    )



# user_online

def user_online(user_id):
    opration = "user_online"

    payload = {
        'user_id':user_id,
        'opration':opration
    }

    client = RpcClient()
    response = client.call(payload)
    decoded_string = response.decode('utf-8')
    data_lists = ast.literal_eval(decoded_string)
    all_rooms = []
    for data_list in data_lists:
        data_list = list(data_list)
        id1 = data_list[0]
        id2 = data_list[1]
        user_ids = [int(id1), int(id2)]
        user_ids = sorted(user_ids)
        room_name = f"chat_{user_ids[0]}-{user_ids[1]}"
        if room_name not in all_rooms:
            all_rooms.append(room_name)
        send_user_status(True, all_rooms)
        
    return "online"


# user_offline

def user_offline(user_id):
    opration = "user_offline"

    payload = {
        'user_id':user_id,
        'opration':opration
    }

    client = RpcClient()
    response = client.call(payload)
    decoded_string = response.decode('utf-8')
    data_lists = ast.literal_eval(decoded_string)
    all_rooms = []
    for data_list in data_lists:
        data_list = list(data_list)
        id1 = data_list[0]
        id2 = data_list[1]
        user_ids = [int(id1), int(id2)]
        user_ids = sorted(user_ids)
        room_name = f"chat_{user_ids[0]}-{user_ids[1]}"
        if room_name not in all_rooms:
            all_rooms.append(room_name)
        send_user_status(False, all_rooms)
    
    return response



# send Call request


def send_call(id, full_name, message):
    group_name = f"notification_{id}"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_call',
            'full_name':full_name,
            'notification': message,
            'service':'call'
        }
    )
    
    
# message triger

def message_triger(id, triger):
    group_name = f"notification_{id}"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'message_online',
            'triger':triger
        }
    )
    
    
    
    
# send user status

def send_user_status(status, group_names):
    for group_name in group_names:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'sent_status',
                'status': status,
            }
        )



# online user


def online_user(user_id):
    opration = "online_user" 
    payload = {
        'user_id':user_id,
        'opration':opration
    }
    client = RpcClient()
    response = client.call(payload)
    return response


# user unview


def user_unview(user_id, chat_user_id):
    opration = "user_unview"
    sender_id = user_id
    receiver_id = chat_user_id
        
    payload = {
                'sender_id':sender_id,
                'receiver_id':receiver_id,
                'opration':opration}
        
    client = RpcClient()
    response = client.call(payload)  
