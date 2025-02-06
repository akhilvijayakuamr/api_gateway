import grpc
from proto.postservice import post_service_pb2, post_service_pb2_grpc
from decouple import config

class APIPostClient:
    def __init__(self):
        self.post_service_channel = grpc.insecure_channel(config('POST_SERVICE_URL'))
        self.post_service_stub = post_service_pb2_grpc.PostServiceStub(self.post_service_channel)
        
        
        
    # Post create
    
    def create_post(self, id, title, content, link, post_image_bytes):
        request = post_service_pb2.CreatePostRequest(
            user_id = int(id),
            title = title,
            post_image = post_image_bytes,
            content = content,
            link = link
        )
        
        return self.post_service_stub.CreatePost(request)
    
    
    
    # Get all post
    
    def get_all_posts(self, user_id):
        request = post_service_pb2.GetAllPostRequest(user_id=int(user_id))
        return self.post_service_stub.GetAllPost(request)
    
    
    
    # Get unique post
    
    def get_unique_post(self, post_id, user_id):
        request = post_service_pb2.GetUniquePostRequest(post_id=post_id,
                                                        user_id = user_id)
        return self.post_service_stub.GetUniquePost(request)
    
    
    # Like post
    
    def like_post(self, post_id, user_id):
        request = post_service_pb2.LikePostRequest(post_id=post_id, user_id=user_id)
        return self.post_service_stub.LikePost(request)
    
    
    # Comment post
    
    def comment_post(self, post_id, user_id, content):
        request = post_service_pb2.CommentPostRequest(post_id=post_id, user_id=user_id, content=content)
        return self.post_service_stub.CommentPost(request)
    
    
    # Replay Comment
    
    def reply_comment(self, user_id, mention_user_id, comment_id, mention_user_fullname, content):
        request = post_service_pb2.CommentReplyRequest(user_id=user_id,
                                                        mention_user_id=mention_user_id,
                                                        comment_id=comment_id,
                                                        mention_user_fullname=mention_user_fullname,
                                                        content=content
                                                        )
    
        return self.post_service_stub.CommentReply(request)
    
    
    # Unique User Posts
    
    def unique_users_posts(self, user_id):
        request = post_service_pb2.UniqueUserPostsRequest(user_id=int(user_id))
        return self.post_service_stub.UniqueUserPosts(request)
    
    
    # Update Post
    
    def update_post(self, id, user_id, title, content, link, post_image_bytes):
        request = post_service_pb2.PostUpdateRequest(
            post_id = int(id),
            user_id = int(user_id),
            title = title,
            post_image = post_image_bytes,
            content = content,
            link = link
        )
        
        return self.post_service_stub.PostUpdate(request)
    
    
    # Comment Delete
    
    def comment_delete(self, comment_id):
        request = post_service_pb2.CommentDeleteRequest(comment_id = int(comment_id))
        return self.post_service_stub.CommentDelete(request)
    
    
    # Reply Delete
    
    def reply_delete(self, reply_id):
        request = post_service_pb2.ReplyDeleteRequest(reply_id = int(reply_id))
        return self.post_service_stub.ReplyDelete(request)
    
    
    
    # Post Delete
    
    def delete_post(self, post_id):
        request = post_service_pb2.PostDeleteRequest(post_id = int(post_id))
        return self.post_service_stub.PostDelete(request)
    
    
    
     # Post Report    
    
    def report_post(self, post_id, report_user_id, reson):
        print(post_id, report_user_id, reson)
        request = post_service_pb2.PostReportRequest(post_id = int(post_id),
                                                    report_user_id = int(report_user_id),
                                                    reson = reson)
        return self.post_service_stub.PostReport(request)
    
    
    # Admin Get all post
    
    def admin_get_all_posts(self):
        request = post_service_pb2.GetAllAdminPostRequest()
        return self.post_service_stub.GetAllAdminPost(request)
    
    
    
    # Post Hide
    
    def hide_post(self, post_id):
        request = post_service_pb2.PostHideRequest(post_id = int(post_id))
        return self.post_service_stub.PostHide(request)
    
    
    
    # Dashboard post all details
    
    def dashboard_post_details(self):
        request = post_service_pb2.DashboardPostDetailsRequest()
        return self.post_service_stub.DashboardPostDetails(request)
    
    
    
    
        
        