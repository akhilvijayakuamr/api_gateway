import grpc 
from proto.userservice import user_service_pb2, user_service_pb2_grpc



class APIUserClient:
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
    
    
    
    
    # Resend OTP
    
    def resend(self, email):
        request = user_service_pb2.ResendOtpRequest(email=email)
        
        return self.user_service_stub.ResendOtp(request)
    
    
    
    
    # User Login
    
    def login_user(self, email, password, provider):
        request = user_service_pb2.LoginUserRequest(email=email,
                                                    password=password,
                                                    provider=provider
                                                   )
        
        return self.user_service_stub.LoginUser(request)
    
    
    
    
    # Admin Login
    
    def login_admin(self, email, password):
        request = user_service_pb2.LoginAdminRequest(email=email,
                                                     password=password
                                                    )
        return self.user_service_stub.LoginAdmin(request)
    
    
    
    
    # Get Allusers
    
    def get_all_users(self):
        request = user_service_pb2.UserListRequest()
        return self.user_service_stub.UserList(request)
    
    
    
    
    
    # Autharization
    
    def check_auth(self, token):
        request = user_service_pb2.AuthRequest(token=token)
        return self.user_service_stub.Autherization(request)
    
    
    
    
    # block and unblock user
    
    def block_unblock_user(self, user_id):
        request = user_service_pb2.BlockUnBlockRequest(id=user_id)
        return self.user_service_stub.BlockUnblockUser(request)
    
    
    
    
    # Get Userprofile datas
    
    def get_profile(self, user_id):
        request = user_service_pb2.ProfileDataRequest(id = user_id)
        return self.user_service_stub.ProfileData(request)





    # User profile update
    
    def update_profile(self, user_id, username, full_name, location, bio, dob, profile, cover):
        request =  user_service_pb2.ProfileUpdateRequest(   id = int(user_id),
                                                            username = username,
                                                            full_name = full_name,
                                                            location = location,
                                                            bio = bio,
                                                            dob = dob,
                                                            profileimage = profile,
                                                            coverimage = cover
                                                        )
        return self.user_service_stub.ProfileUpdate(request)
                                                                
    
    
    
    
    # Google auth
    
    def google_user(self, email, fullname):
        request = user_service_pb2.GoogleUserRequest(email=email,
                                                    full_name=fullname,
                                                   )
        
        return self.user_service_stub.GoogleUser(request)
    
    
    
    
    # ForgotEmail
    
    def user_forgot(self, email):
        request = user_service_pb2.ForgoteEmailRequest(email=email)
        return self.user_service_stub.ForgotEmail(request)
    
    
    
    
    
    # Change Email
    
    def change_password(self, email, password):
        request = user_service_pb2.ChangePasswordRequest(email=email,
                                                         password=password)
        return self.user_service_stub.ChangePassword(request)
    
    
    
    
    
    # Take user profile photo

    def profile_photo(self, user_id):
        request = user_service_pb2.PostProfileRequest(user_id=user_id)
        return self.user_service_stub.PostProfile(request)
    
    
    
    
    
    # Take unique post data
    
    def post_unique_data(self, user_id):
        request = user_service_pb2.PostUniqueDataRequest(user_id = user_id)
        response = self.user_service_stub.PostUniqueData(request)    
        return response
    
    
    
    
    
    # Take Comment user data
    
    def comment_data(self, user_id):
        request = user_service_pb2.CommentUniqueDataRequest(user_id=user_id)
        return self.user_service_stub.CommentUniqueData(request)
    
    
        
    
  
    

        
    
    
    