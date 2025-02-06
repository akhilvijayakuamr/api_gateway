from api_gateway.auth import authorization
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
import json
from .service import *
from userservice.service import APIUserClient
from .serializers import ChatUserSerializer
from grpc import RpcError
import grpc
import stripe
from django.shortcuts import redirect
from django.conf import settings
from stripe.error import StripeError
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


userclient = APIUserClient()
stripe.api_key = settings.STRIP_SECRET_KEY
FRONT_END_URL = settings.FRONT_END_URL




# Take specific chat list

class ChatList(APIView):
    def post(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                sender_id = request.data.get('userId')
                receiver_id = request.data.get('chatUserId')
                response = chat_list(sender_id, receiver_id)
                if isinstance(response, bytes):
                    decoded_string = response.decode('utf-8')
                elif isinstance(response, list): 
                    decoded_string = response

                if decoded_string:
                    decoded_string = decoded_string.replace("'", '"') 
                    decoded_string = decoded_string.replace('False', 'false').replace('True', 'true')
                    parsed_data = json.loads(decoded_string)
                else:
                    parsed_data = [] 
                return Response(parsed_data, status=status.HTTP_200_OK) 
            else:
                return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED) 
         
        except RpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                return Response("Authentication failed", status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        




# Get all chat users


class ChatUserList(APIView):
     def post(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                user_id = request.data.get('userId')
                
                response = all_chat_user(user_id)
                if isinstance(response, bytes):
                    decoded_string = response.decode('utf-8')
                    decoded_string = decoded_string.replace("'", '"').replace("False", "false").replace("True", "true")
                elif isinstance(response, list):
                    decoded_string = response
                if decoded_string:
                    try:
                        parsed_data = json.loads(decoded_string) 
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
                        parsed_data = []
                chat_users = []
                for user in parsed_data:
                    user_id = user[0]
                    profile_response =  userclient.post_unique_data(user_id)

                    users = {
                        'id':user_id,
                        'user_profile':profile_response.profile_image,
                        'full_name':profile_response.full_name,
                        'message':int(user[1]),
                        'online':user[2]
                                     
                    }

                    chat_users.append(users)

                serializer = ChatUserSerializer(chat_users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED) 
            
        except RpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                return Response("Authentication failed", status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        




# Get all notifications


class GetNotifications(APIView):
     def post(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                user_id = request.data.get('userId')
                response =  get_all_notification(user_id) 
                if isinstance(response, bytes):
                    decoded_string = response.decode('utf-8')
                    decoded_string = decoded_string.replace("None", "null") 
                    decoded_string = decoded_string.replace("'", '"') 
                    decoded_string = decoded_string.replace("False", "false") 
                    decoded_string = decoded_string.replace("True", "true") 
                elif isinstance(response, list): 
                    decoded_string = response
                else:
                    decoded_string = []
                if decoded_string:
                    try:
                        parsed_data = json.loads(decoded_string) 
                    except json.JSONDecodeError as e:
                        print(f"Error parsing JSON: {e}")
                        parsed_data = []
                else:
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
                return Response(notifications, status=status.HTTP_200_OK) 
            else:
                return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED)
         
        except RpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                return Response("Authentication failed", status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
             
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        


# Read all notification


class ReadNotification(APIView):
     def post(self, request):
        try:
            auth = authorization(request)
            print(auth)
            if auth.user:
                user_id = request.data.get('userId')
                
                response = read_all_notification(user_id)
                return Response({"message":"Read all notifications"}, status=status.HTTP_200_OK)
            else:
                return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED) 
            
        except RpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                return Response("Authentication failed", status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            
            
            
# user is online


class OnlineUser(APIView):
     def post(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                user_id = request.data.get('user_id')
                response = online_user(user_id)
                decoded_response = response.decode('utf-8')
                is_user_online = decoded_response == 'True'
                return Response({"online":is_user_online}, status=status.HTTP_200_OK)
            else:
                return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED) 
        except RpcError as e:
            if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                return Response("Authentication failed", status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            
            
            
        
        
# Strip Checkout view


class StripeCheckoutView(APIView):

    def post(self, request):
        try:
            checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price': 'price_1QQRdnJqqRzLhxPC2DWV0po8',
                    'quantity': 1,
                },
            ],
            payment_method_types=['card'],
            mode='subscription',
            success_url = "https://assuretech.cyou/payment_success",
            cancel_url = "https://assuretech.cyou/payment_failed"
        )
            return redirect(checkout_session.url)

        except StripeError as e:
            print("url of front end =",FRONT_END_URL)
            print(f"Stripe error occurred: {e.error.message}")  # More specific error message from Stripe
            return Response({"error": e.user_message or "Stripe error occurred"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print("it is worked")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        


# Strip webhook view

class StripeWebhookView(APIView):
    csrf_exempt = True

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        endpoint_secret = settings.WEB_HOOKS_SECRET_KEY  

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, endpoint_secret
            )
        except ValueError as e:
            return Response({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return Response({"error": "Invalid signature"}, status=400)

        
        if event['type'] == 'checkout.session.completed':
            session = event['data']['object']
            self.handle_successful_payment(session)
        return Response({"status": "success"}, status=200)
    
    
    # Payment success operation

    def handle_successful_payment(self, session):
        customer_id = session.get('customer', '')
        email = session.get('customer_details', {}).get('email', '')
        amount_total = session.get('amount_total', 0)
        if isinstance(amount_total, tuple):
            amount_total = int(amount_total[0])  
        elif isinstance(amount_total, str):
            amount_total = int(amount_total)  
        amount = amount_total / 100 
        currency = session.get('currency', 'INR')
        payment_status = session.get('payment_status', 'unpaid')
        response = premium(customer_id, email, amount, currency, payment_status)
        return response

        
        
# Check premium

class CheckPremium(APIView):
        def post(self, request):
            try:
                auth = authorization(request)
                if auth.user:
                    email = request.data.get('email')
                    response = premium_user(email)
                    decoded_response = response.decode('utf-8')
                    is_user_online = decoded_response == 'True'
                    return Response({"premium":is_user_online}, status=status.HTTP_200_OK)
                else:
                    return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED) 
            except RpcError as e:
                if e.code() == grpc.StatusCode.UNAUTHENTICATED:
                    return Response("Authentication failed", status=status.HTTP_401_UNAUTHORIZED)
                return Response({
                    "error": f"{e.details()}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            except Exception as e:
                return Response({
                    "error": f"An unexpected error occurred: {str(e)}"
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            
        


        
        
          








            
             
        


