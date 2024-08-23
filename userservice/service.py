import grpc 
from proto.userservice import user_service_pb2, user_service_pb2_grpc



class APIclient:
    def __init__(self):
        self.user_service_channel = grpc.insecure_channel('localhost:50051')
        self.user_service_stub = user_service_pb2_grpc.UserServiceStub(self.user_service_channel)
        
        
    # User Register
        
    def create_user(self, email, username, full_name, password):
        
        request = user_service_pb2.CreateUserRequest(email=email,
                                                     username=username,
                                                     full_name=full_name,
                                                     password=password
                                                    )
        
        return self.user_service_stub.CreateUser(request)
    
    
    # Verify OTP
    
    def verify_otp(self, email, otp):
        
        request = user_service_pb2.VerifyOtpRequest(email=email,
                                                    otp=otp
                                                   )
        
        return self.user_service_stub.VerifyOtp(request)
    
    
    # User Login
    
    
    def login_user(self, email, password, provider):
        
        request = user_service_pb2.LoginUserRequest(email=email,
                                                    password=password,
                                                    provider=provider
                                                   )
        
        return self.user_service_stub.LoginUser(request)
    
    
    