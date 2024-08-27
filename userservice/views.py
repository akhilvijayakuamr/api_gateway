from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import APIclient
from grpc import RpcError



# Create your views here.


client = APIclient()

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
            return Response({"Message": {response.message},
                             "error":{response.error}
                             }, status=status.HTTP_201_CREATED)
        
        except RpcError as e:
            return Response({
                "error": f"gRPC error occurred: {e.details()}"
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
                "error": f"gRPC error occurred: {e.details()}"
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
                    "email": response.email
                }, status=status.HTTP_200_OK)
        
        except RpcError as e:
            return Response({
                "error": f"gRPC error occurred: {e.details()}"
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
                "error": f"gRPC error occurred: {e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    


