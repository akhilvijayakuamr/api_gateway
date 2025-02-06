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
    operation = "create_room"
        
    payload = {
                'sender_id':sender_id,
                'receiver_id':receiver_id,
                'operation':operation}
        
    client = RpcClient()
    response = client.call(payload)  
    return response


# Message save


def message_save(user_id, chat_user_id, message):
    sender_id = user_id
    receiver_id = chat_user_id
    message_content = message
    operation = "save_message"
    
    payload = {
                'sender_id':sender_id,
                'receiver_id':receiver_id,
                'message_content':message_content,
                'operation':operation}
    
        
    client = RpcClient()
    response = client.call(payload)
    decoded_string = response.decode('utf-8')
    data_list = ast.literal_eval(decoded_string)
    if(data_list):
        message_triger(receiver_id, data_list)
    return data_list
    



    
# Message object

def message_obj(message_content):
    message_content = message_content
    operation = "get_message"
    
    payload = {
        'message_content':message_content,
        'operation':operation
    }
    
    client = RpcClient()
    response = client.call(payload)
    return response



# Get specific user chat


def chat_list(sender_id, receiver_id):

    operation = "get_all_chat"

    payload = {
            'sender_id':sender_id,
            'receiver_id':receiver_id,
            'operation':operation
                }
                
    client = RpcClient()
    response = client.call(payload)
    return response



# Get all user chat

def all_chat_user(user_id):

    operation = "all_chat_user"

    payload = {
        'user_id':user_id,
        'operation':operation
    }

    client = RpcClient()
    response = client.call(payload)
    return response



# Notification for followers

def follow_notification(user_id, another_user_id):
    operation = "follow_notification"

    payload = {
        'user_id':user_id,
        'another_user_id':another_user_id,
        'operation':operation
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
        'operation':opration
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
    operation = "comment_notification"
    payload = {
        'user_id':user_id,
        'another_user_id':another_user_id,
        'post_id':post_id,
        'operation':operation
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

    operation = "all_notification"

    payload = {
        'user_id':user_id,
        'operation':operation
    }

    client = RpcClient()
    response = client.call(payload)
    return response




# Read notifications

def read_all_notification(user_id):

    operation = "read_notification"

    payload = {
        'user_id':user_id,
        'operation':operation
    }

    client = RpcClient()
    response = client.call(payload)
    return response




# Notifiation object

def notification_obj(notification_content):
    notification_content = notification_content
    operation = "get_notification"
    
    payload = {
        'notification_content':notification_content,
        'operation':operation
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
    operation = "user_online"

    payload = {
        'user_id':user_id,
        'operation':operation
    }

    client = RpcClient()
    response = client.call(payload)
    if isinstance(response, bytes):
        decoded_string = response.decode('utf-8')
        data_lists = ast.literal_eval(decoded_string)
    elif isinstance(response, list): 
        data_lists = response
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
    send_user_status(True, all_rooms, user_id)
        
    return "online"


# user_offline

def user_offline(user_id):
    operation = "user_offline"

    payload = {
        'user_id':user_id,
        'operation':operation
    }

    client = RpcClient()
    response = client.call(payload)
    if isinstance(response, bytes):  
        decoded_string = response.decode('utf-8')
        data_lists = ast.literal_eval(decoded_string)
    elif isinstance(response, list):
        data_lists = response
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
        send_user_status(False, all_rooms, user_id)
    return response



# send Call request


def send_call(id, full_name, message, caller_id):
    group_name = f"notification_{id}"
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': 'send_call',
            'full_name':full_name,
            'notification': message,
            'my_id':id,
            'caller_id':caller_id,
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

def send_user_status(status, group_names, user_id):
    for group_name in group_names:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': 'sent_status',
                'status': {"status":status,
                           "user_id":user_id},
            }
        )


# online user

def online_user(user_id):
    operation = "online_user" 
    payload = {
        'user_id':user_id,
        'operation':operation
    }
    client = RpcClient()
    response = client.call(payload)
    return response


# user unview

def user_unview(user_id, chat_user_id):
    operation = "user_unview"
    sender_id = user_id
    receiver_id = chat_user_id
        
    payload = {
                'sender_id':sender_id,
                'receiver_id':receiver_id,
                'operation':operation}
        
    client = RpcClient()
    response = client.call(payload)  
    
    
# Premium customer

def premium(customer_id, email, amount, currency, status):
    operation = "premium"
    
    payload = {
        'customer_id':customer_id, 
        'email':email,
        'amount':amount, 
        'currency':currency, 
        'status':status,
        'operation':operation
    }
    
    client = RpcClient()
    return client.call(payload)  


# Check premium

def premium_user(email):
    operation = "premium_user" 
    payload = {
        'email':email,
        'operation':operation
    }
    client = RpcClient()
    response = client.call(payload)
    return response
