from django.http import JsonResponse
from .rabbitmq import RpcClient
from api_gateway.auth import authorization
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import json
from .service import *
from userservice.service import APIUserClient
from .serializers import ChatUserSerializer, NotificationSerializer


userclient = APIUserClient()



# Take specific chat list

class ChatList(APIView):
    def post(self, request):
        try:
            # auth = authorization(request)
            # print(auth)
            # if auth.user:
                sender_id = request.data.get('userId')
                receiver_id = request.data.get('chatUserId')
                
                response = chat_list(sender_id, receiver_id)
                
                decoded_string = response.decode('utf-8')

                if decoded_string:
                    decoded_string = decoded_string.replace("'", '"') 
                    decoded_string = decoded_string.replace('False', 'false').replace('True', 'true')
                    parsed_data = json.loads(decoded_string)
                else:
                    parsed_data = [] 
                return Response(parsed_data, status=status.HTTP_200_OK) 
            # else:
            #     return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED) 
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        




# Get all chat users


class ChatUserList(APIView):
     def post(self, request):
        try:
            # auth = authorization(request)
            # print(auth)
            # if auth.user:
                user_id = request.data.get('userId')
                
                response = all_chat_user(user_id)
                
                decoded_string = response.decode('utf-8')
                
                decoded_string = decoded_string.replace('False', 'false').replace('True', 'true').replace('{', '[').replace('}', ']')
                

                try:
                    parsed_data = json.loads(decoded_string) 
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
                    parsed_data = []

                chat_users = []

                for user in parsed_data:
                    user_id = user[1]
                    profile_response =  userclient.post_unique_data(user_id)

                    users = {
                        'id':user_id,
                        'user_profile':profile_response.profile_image,
                        'full_name':profile_response.full_name,
                        'online':user[0]
                    }
                    print(users)

                    chat_users.append(users)

                serializer = ChatUserSerializer(chat_users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            # else:
            #     return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED) 
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        




# Get all notifications


class GetNotifications(APIView):
     def post(self, request):
        try:
            # auth = authorization(request)
            # print(auth)
            # if auth.user:
            user_id = request.data.get('userId')
            response =  get_all_notification(user_id) 
            decoded_string = response.decode('utf-8')
            decoded_string = decoded_string.replace("None", "null") 
            decoded_string = decoded_string.replace("'", '"') 
            decoded_string = decoded_string.replace("False", "false") 
            decoded_string = decoded_string.replace("True", "true") 

            try:
                parsed_data = json.loads(decoded_string) 
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                parsed_data = []

            notifications = []
            for notification in parsed_data:
                user_id = notification.get('another_user') 
                profile_response =  userclient.post_unique_data(user_id)
                
                data = {
                    "id":notification.get('another_user'),
                    "another_user":notification.get('another_user'),
                    "follower":notification.get('follower'),
                    "post":notification.get('post'),
                    "content":notification.get('content'),
                    "timestamp":notification.get('timestamp'),
                    "read":notification.get('read'),
                    "user_profile":profile_response.profile_image,
                    "full_name":profile_response.full_name,

                }

                notifications.append(data)

                

            # serializer = NotificationSerializer(notifications, many=True)
            # print("sadfasfasfsafasfsaf",serializer.data)
            return Response(notifications, status=status.HTTP_200_OK)
                              
            # else:
            #     return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED) 
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        


# Read all notification


class ReadNotification(APIView):
     def post(self, request):
        try:
            # auth = authorization(request)
            # print(auth)
            # if auth.user:
                user_id = request.data.get('userId')
                
                response = read_all_notification(user_id)
                return Response({"message":"Read all notifications"}, status=status.HTTP_200_OK)
            # else:
            #     return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED) 
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
        
          








            
             
        


