from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import APIUserClient
from grpc import RpcError
from .serializers import *
from api_gateway.auth import authorization
from postservice.service import APIPostClient
from postservice.serilizers import PostSerializers
from communication_service.service import follow_notification
import grpc



# Create your views here.

client = APIUserClient()
post_client = APIPostClient()



# User register

class CreateUserView(APIView):
    def post(self, request):
        email, username, full_name, password, conform_password = self.extract_data(request)
        
        validation_error = self.validate_fields(email, username, full_name, password, conform_password)
        
        if validation_error:
            return validation_error
       
        if not self.is_valid_password(password):
            return Response({'error': 'Password must be at least 8 characters long and contain at least one uppercase letter, one lowercase letter, and one digit'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        try:
            response = client.create_user(email=email,
                                        username=username,
                                        full_name=full_name,
                                        password=password
                                        )
            return Response({"Message": {response.message}}, status=status.HTTP_201_CREATED)
        
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
    
    
    
    # validate password           
                
    def is_valid_password(self, password):
        return (
            len(password) >= 8 and
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password)
        )
    
    
    
    
    # Extracting data
    
    def extract_data(self, request):
        return (
            request.data.get('email'),
            request.data.get('username'),
            request.data.get('name'),
            request.data.get('password'),
            request.data.get('confirmPassword'),
        )            
           
           
           
           
                
    # validation Function           
                
    def validate_fields(self, email, username, full_name, password, conform_password):
        if (not email or not email.strip()):
            return Response({"error":"Email is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if (not username or not username.strip()):
            return Response({"error":"Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if (not full_name or not full_name.strip()):
            return Response({"error":"Full name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if (not password or not password.strip()):
            return Response({"error":"Password is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if (not conform_password or not conform_password.strip()):
            return Response({"error":"Conform password is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if (password != conform_password):
            return Response({"error":"Password mismatch"}, status=status.HTTP_400_BAD_REQUEST)
        
        return None
    
    
    
    
    
# OTP varification view
                    
class OtpVerification(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        
        if not otp:
            return Response({'error':'Please enter otp'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            response = client.verify_otp(email=email,
                                         otp=otp
                                        )
            return Response({f"Response Message: {response.message}"}, status=status.HTTP_201_CREATED)
        
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
           
           
           
            
 
# Resend OTP view           
            
class ResendOtp(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        if not email:
            return Response("Please Register Again !!", status=status.HTTP_404_NOT_FOUND)
        
        try:
            response = client.resend(email=email)
            return Response(f"Response Message: {response.message}", status=status.HTTP_200_OK)
        
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        
            
            
            
# User Login view

class UserLoginView(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        provider = request.data.get('provider')
        
        if not email or not email.strip():
            return Response({'error':'Email Not Found Please Login Again'})
        
        if not password or not password.strip():
            return Response({'error':'Password Not Found Please Login Again'})
        
        try:
            response = client.login_user(email=email,
                                         password=password,
                                         provider=provider
                                        )
            
            return Response({
                    "message": response.message,
                    "access_token": response.access_token,
                    "refresh_token":response.refresh_token,
                    "id": response.id,
                    "email": response.email,
                    "profile_image":response.profile
                }, status=status.HTTP_200_OK)
        
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            



# Admin Login view

class AdminLoginView(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not email or not email.strip():
            return Response({'error':'Email Not Found Please Login Again'})
        
        if not password or not password.strip():
            return Response({'error':'Password Not Found Please Login Again'})
        
        try:
            
            response = client.login_admin(email=email,
                                          password=password
                                         )
            
            return Response({
                    "message": response.message,
                    "access_token": response.access_token,
                    "refresh_token":response.refresh_token,
            }, status=status.HTTP_200_OK)
            
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            
            
# User list view

class UserListView(APIView):
    
    def get(self, request):
        try:
            auth = authorization(request)
            if auth.admin:
                response = client.get_all_users()
                serializer = UserListSerializer(response.users, many=True)
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
            
            
        
        
            
# block and unblock

class BlockUnBlockView(APIView):
    
    
    def post(self, request):
        try:
            auth = authorization(request)
            
            if auth.admin:
                user_id = request.data.get('userId')
                response = client.block_unblock_user(user_id)
                return Response({"message":response.message}, status=status.HTTP_200_OK)
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
            
            
            
        
            
# User profile data

class UserProfileData(APIView):
    def post(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                user_id = request.data.get('userId')
                profile_id = request.data.get('profileId')
                response = client.get_profile(int(user_id), int(profile_id))
                
                post = post_client.unique_users_posts(profile_id)
                all_posts = post.posts
                
                post_details = []
                for post in all_posts:
                    profile_response = client.profile_photo(post.user_id)
                    
                    formatted_date = post.date[:10]
              
                    details = {
                        "post_id" :post.post_id,
                        "user_id" :post.user_id,
                        "title" : post.title,
                        "content" :post.content,
                        "link" :post.link,
                        "date" :formatted_date,
                        "postimage" :post.postimage,
                        "profileimage":profile_response.profile_image if profile_response.profile_image else '',
                        "like":post.like if post.like else False,
                        'like_count':post.like_count if post.like_count else 0,
                        'comment_count':post.comment_count if post.comment_count else 0
                                             
                    }
                    post_details.append(details)   
                    
                serializer = PostSerializers(post_details, many=True)
             
                
                if serializer.is_valid:
                    posts = serializer.data
                
                
                data = {
                    'id':str(response.id),
                    'username':response.username,
                    'full_name':response.full_name,
                    'location':response.location,
                    'bio':response.bio,
                    'dob':response.dob,
                    'profileImage':response.profileimage,
                    'coverImage':response.coverimage,
                    'follow':response.follow,
                    'followers_count':response.followers_count,
                    'following_count':response.following_count,
                    'posts':posts
                    
                }
                
                return Response(data, status=status.HTTP_200_OK)
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
            
   
   
   
            
# User update view

class UserUpdateView(APIView):
    def put(self, request):
        try:
            auth = authorization(request)
            
            if auth.user:  
                user_id = request.data.get('userId') if request.data.get('userId') else ''
                username = request.data.get('username') if request.data.get('username') else ''
                full_name = request.data.get('full_name') if request.data.get('full_name') else ''
                location = request.data.get('location') if request.data.get('location') else ''
                bio = request.data.get('bio') if request.data.get('bio') else ''
                dob = request.data.get('dob') if request.data.get('dob') else ''
                profile_image = request.FILES.get('profileImage') if request.FILES.get('profileImage') else b''
                cover_image = request.FILES.get('coverImage') if request.FILES.get('coverImage') else b''
                profile_image_bytes = profile_image.read() if profile_image else b''
                cover_image_bytes = cover_image.read() if cover_image else b''
                
                try:
                
                    response = client.update_profile(user_id, username, full_name, location, bio, dob, profile_image_bytes, cover_image_bytes)
                    return Response(f"{response.message}", status=status.HTTP_200_OK)
                         
                except RpcError as e:
                    return Response({
                     "error": f"{e.details()}"
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
                except Exception as e:
                    return Response({
                    "error": f"An unexpected error occurred: {str(e)}"
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            else:
                return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED) 
            
        except authorization:
            return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED)
           
            
    
            

# Google auth

class GoogleLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        fullname = request.data.get('fullname')
        
        if not email or not email.strip():
            return Response({'error':'Email Not Found Please Login Again'})
        if not fullname or not fullname.strip():
            return Response({'error':'Password Not Found Please Login Again'})
        try:
            
            response = client.google_user(email=email,
                                         fullname=fullname,
                                        )
            
            return Response({
                    "access_token":response.access_token,
                    "refresh_token":response.refresh_token,
                    "message": response.message,
                    "id": response.id,
                    "email": response.email
                }, status=status.HTTP_200_OK)
        
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            



# User forgot email

class UserForgotView(APIView):
    def post(self, request):
        email = request.data.get('email')
        
        if not email or not email.strip():
            return Response({'error':'Email Not Found Please Login Agian'})
        
        try:
            response = client.user_forgot(email)
            return Response({"message": {response.message}
                             }, status=status.HTTP_201_CREATED)
        
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            
            
# Change password view         
            
class ChangePassword(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        
        if not password or not password.strip():
            return Response("{'error':'Password Not Found Please Enter Password}")
        
        try:
            response = client.change_password(email, password)
            return Response({"message": {response.message}
                             }, status=status.HTTP_201_CREATED)
            
            
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
# User Follow

class UserFollow(APIView):
    def post(self, request):
        user_id = request.data.get('userId')
        follow_user_id = request.data.get('followUserId')
        
        if not user_id or not follow_user_id:
             return Response("{'error':'The argument is not found'}")
        
        try:
            response = client.follow_user(user_id, follow_user_id)
            if response.message == "You are now following this user":
                result = follow_notification(user_id, follow_user_id)
            return Response({"message": {response.message}
                             }, status=status.HTTP_201_CREATED)
            
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


# Search User

class SearchUser(APIView):
    def post(self, request):
        query = request.data.get('query')
        user_id = request.data.get('userId')

        if not query or not user_id:
            return Response("{'error':'The argument is not found'}", status=status.HTTP_404_NOT_FOUND)
        
        try:
            response = client.search_user(query, user_id)
            search_users = []
            for user in response.searchdata:
                user = {
                    "id" : user.id,
                    "full_name" : user.full_name,
                    "username" : user.user_name,
                    "user_profile" : user.user_profile
                }

                search_users.append(user)

            serializer = UserDataSerializer(search_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            




# Get all followers and followings

class GetFriends(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response("{'error':'The argument is not found'}", status=status.HTTP_404_NOT_FOUND)
        
        try:
            response = client.get_friends(user_id)
            follower_list = []
            for follower in response.follower:
                user ={
                    "id":follower.id,
                    "full_name":follower.full_name,
                    "username":follower.user_name,
                    "user_profile":follower.user_profile
                }
                
                follower_list.append(user)
            
            followed_list = []
            for followed in response.followed:
                user ={
                    "id":followed.id,
                    "full_name":followed.full_name,
                    "username":followed.user_name,
                    "user_profile":followed.user_profile
                }
                
                followed_list.append(user)
                
            friend_list ={
                "follower":follower_list,
                "followed":followed_list
            }
            
            serializer = UserFriendsSerializer(friend_list)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            
            
# Create new access token

class CreateAccessToken(APIView):
    def get(self, request):
        try:    
            auth_header = request.headers.get('Authorization')
            if not auth_header or 'Bearer ' not in auth_header:
                return Response({'error':'Email Not Found Please Login Again'})
            token = auth_header.split('Bearer ')[1].strip()
            
            response = client.check_refresh(token)
            
            return Response({"access_token":response.access_token,
                             "refresh_token":response.refresh_token}, status=status.HTTP_200_OK)
            
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
            
    
            
            
# Get all dashboard user details

class DashboardUserData(APIView):
    def get(self, request):
    
        try:
            auth = authorization(request)
            if auth.admin:
                user_response = client.dashboard_user_details()
                post_response = post_client.dashboard_post_details()
                data = {
                    "all_users" : user_response.all_users,
                    "block_users" : user_response.block_users,
                    "all_posts" : post_response.all_posts,
                    "hide_posts" : post_response.hide_posts,
                    "deleted_posts" : post_response.deleted_posts,
                    "reported_post" : post_response.reported_posts,
                    "all_reports" :post_response.all_reports
                }
                
                serializer = DashboardSerializer(data)
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
            
            
               
            
            
            
         
         
        
            



        
        
    


