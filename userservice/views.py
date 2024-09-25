from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import APIUserClient
from grpc import RpcError
from .serializers import UserListSerializer
from api_gateway.auth import authorization



# Create your views here.

client = APIUserClient()



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
                    "token": response.jwt,
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
                "message":response.message,
                "token": response.jwt
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
                response = client.get_profile(int(user_id))
                data = {
                    'id':str(response.id),
                    'username':response.username,
                    'full_name':response.full_name,
                    'location':response.location,
                    'bio':response.bio,
                    'dob':response.bio,
                    'profileImage':response.profileimage,
                    'coverImage':response.coverimage
                }
                
                print("data", data)
                
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED)  
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
            
   
   
   
            
# User update view

class UserUpdateView(APIView):
    def post(self, request):
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
                    "message": response.message,
                    "token": response.jwt,
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



        
        
    


