import grpc
from proto.postservice import post_service_pb2, post_service_pb2_grpc


class APIPostClient:
    def __init__(self):
        self.post_service_channel = grpc.insecure_channel('localhost:50052')
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
    
    
    
    
    
        
        