from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from grpc import RpcError
from api_gateway.auth import authorization
from .service import APIPostClient
from userservice.service import APIUserClient
from . serilizers import PostSerializers, CommentSerializer, ReplaySerializer
from datetime import datetime
from communication_service.service import like_notification, comment_notification
import grpc


# Create your views here.

client = APIPostClient()
userclient = APIUserClient()


# Create Post

class CreatePost(APIView):
    def post(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                id = request.data.get('id')
                title =  request.data.get('title')
                content = request.data.get('content')
                link  = request.data.get('link')
                post_image = request.FILES.get('postImage')
                post_image_bytes = post_image.read()
            
                try:
                    response = client.create_post(id, title, content, link, post_image_bytes)
                    return Response({'message': response.message, 'post_id': str(response.post_id)}, status=status.HTTP_201_CREATED)
                    
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
        
        
        

# Get all post

class GetAllPost(APIView):
    def post(self, request):
        try:
            auth = authorization(request)
            print("auth")
            if auth.user:
                user_id = request.data.get('userId')
                
                response = client.get_all_posts(user_id)
            
                
                all_posts = response.posts
                
                post_details = []
                for post in all_posts:
                    profile_response = userclient.profile_photo(post.user_id)
                    
                    
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
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Data in not found", status=status.HTTP_404_NOT_FOUND)
                    
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
            
            
            
       
# Get unique post

class GetUniquePost(APIView):
    def post(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                post_id =  request.data.get('postId')
                user_id = request.data.get('userId')
                response = client.get_unique_post(int(post_id), int(user_id))
                profile_response =  userclient.post_unique_data(response.user_id)
                formatted_date = response.date[:10]
        
                comment_list = []
                
                for comment in response.comments:
                    comment_formatted_date = comment.date[:10]
                    comment_response = userclient.comment_data(comment.user_id)
                    
                    replay_list = []
                    
                    for reply in comment.replies:
                        reply_response = userclient.comment_data(reply.user_id)
                        
                        
                        # Replies all details
                        reply_details = {
                            "replay_id": reply.replay_id,
                            "user_id": reply.user_id,
                            "mention_user_id": reply.mention_user_id,
                            "mention_user": reply.mention_user,
                            "content": reply.content,
                            "date": reply.date,
                            "full_name":reply_response.full_name,
                            "user_profile":reply_response.user_profile, 
                        }
                        
                        replay_list.append(reply_details)
                    
                    # Comment all details 
                    details = {
                        "comment_id":comment.comment_id,
                        "user_id":comment.user_id,
                        "content":comment.content,
                        "date":comment_formatted_date,
                        "full_name":comment_response.full_name,
                        "user_profile":comment_response.user_profile, 
                        "reply_count":comment.reply_count,
                        "replies":replay_list
                    }
                    
                    comment_list.append(details)
                      
                # post all details
                data = {
                    'post_id':response.post_id,
                    'user_id':response.user_id,
                    'title':response.title,
                    'content':response.content,
                    'link':response.link,
                    'date':formatted_date,
                    'postimage':response.postimage,
                    'profileimage':profile_response.profile_image,
                    'bio':profile_response.bio,
                    'full_name':profile_response.full_name,
                    'username':profile_response.username,
                    'like':response.like,
                    'like_count':response.like_count if response.like_count else 0,
                    'comment_count':response.comment_count if response.comment_count else 0,
                    'comments': comment_list
                }
                
                
                serializer = PostSerializers(data=data)
                
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Data in not found", status=status.HTTP_404_NOT_FOUND)
                
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
            
            
            
            
# Like post

class LikeApiView(APIView):
    def post(self, request):
        try:
            auth = authorization(request)
            
            if auth.user:
                post_id = request.data.get('postId')
                user_id = request.data.get('userId')
                response = client.like_post(int(post_id), int(user_id))

                if (response.user_id != int(user_id) and response.message == 'like post'):
                    data=like_notification(response.user_id,user_id,post_id)

                return Response(f"{response.message}", status=status.HTTP_201_CREATED)
            
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
            
            
            
            
# Comment post

class CommentApiView(APIView):
    def post(self, request):
        try:
            auth = authorization(request)
            
            if auth.user:
                post_id = request.data.get('postId')
                user_id = request.data.get('userId')
                content = request.data.get('content')
                response = client.comment_post(int(post_id), int(user_id), content)
                comment_response = userclient.comment_data(response.id)

                data ={
                    "comment_id":response.comment_id,
                    "user_id" : response.id,
                    "content" : response.content,
                    "date" : response.date,
                    "full_name":comment_response.full_name,
                    "user_profile":comment_response.user_profile, 
                    "reply_count" : response.reply_count,
                    "replies" : []
                }

                serializer = CommentSerializer(data)
                if(int(user_id)!=response.user_id):
                    result = comment_notification(response.user_id, user_id, post_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
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
            
            
            
            
# Comment Replay

class CommentReply(APIView):
    
    def post(self, request):
        try:
            auth = authorization(request)
            
            if auth.user:
                user_id = request.data.get('userId')
                mention_user_id = request.data.get('mentionUserId')
                comment_id = request.data.get('commentId')
                mention_user_fullname = request.data.get('mentionUserFullName')
                content = request.data.get('content')

                response=client.reply_comment(int(user_id),
                                      int(mention_user_id),
                                      int(comment_id), 
                                      mention_user_fullname, 
                                      content)
                
                
                user_response = userclient.comment_data(response.user_id)
                

                data = {
                    "replay_id" : response.reply_id,
                    "user_id" : response.user_id,
                    "mention_user_id" : response.mention_user_id,
                    "mention_user" : response.mention_user_full_name,
                    "content" : response.content,
                    "date" : response.date,
                    "full_name" : user_response.full_name,
                    "user_profile" : user_response.user_profile,
                    "comment_id":response.comment_id
                }

                serializer = ReplaySerializer(data)

                return Response(serializer.data, status=status.HTTP_201_CREATED)  
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
            
            
            
            
# Post Update

class UpdatePost(APIView):
    def put(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                id = request.data.get('id')
                user_id = request.data.get('user_id')
                title =  request.data.get('title') if request.data.get('title') else ''
                content = request.data.get('content') if request.data.get('content') else ''
                link  = request.data.get('link') if request.data.get('link') else ''
                post_image = request.FILES.get('postImage') if request.FILES.get('postImage') else b''
                post_image_bytes = post_image.read() if post_image else b''
            
                try:
                    response = client.update_post(id, user_id, title, content, link, post_image_bytes)
                    return Response({'message': response.message, 'post_id': str(response.post_id)}, status=status.HTTP_201_CREATED)
                    
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
        
        
        

# Delete Comment

class DeleteComment(APIView):
    def delete(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                comment_id = request.data.get('commentId')
                response = client.comment_delete(comment_id)
                return Response(f"{response.message}", status=status.HTTP_200_OK)
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
            
            
            
            
# Delete Reply
    
class DeleteReply(APIView):
    def delete(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                reply_id = request.data.get('replyId')
                response = client.reply_delete(reply_id)
                return Response(f"{response.message}", status=status.HTTP_200_OK)
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
                
                    
            

# Delete Post

class DeletePost(APIView):
    def delete(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                post_id = request.data.get('postId')
                response = client.delete_post(post_id)
                return Response(f"{response.message}", status=status.HTTP_200_OK)
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
                



# Report Post

class ReportPost(APIView):
    def post(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                post_id = request.data.get('postId')
                report_user_id = request.data.get('reportUserId')
                reson = request.data.get('report')
                response = client.report_post(post_id, report_user_id, reson)
                return Response(f"{response.message}", status=status.HTTP_200_OK)
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
            



# Get all post

class GetAdminAllPost(APIView):
    def get(self, request):
        try:
            auth = authorization(request)
            if auth.admin:
                response = client.admin_get_all_posts()
                all_posts = response.posts
                
                post_details = []
                for post in all_posts:
                    profile_response = userclient.profile_photo(post.user_id)
                    formatted_date = post.date[:10]
                    
                    
                    report_list = []
                    
                    for report in post.reports:
                        report_response = userclient.comment_data(report.report_user_id)
                        
                        
                        # Report all details
                        report_details = {
                            "report_id": report.report_id,
                            "report_user_id": report.report_user_id,
                            "reson": report.reason,
                            "date": report.created_at,
                            "full_name":report_response.full_name,
                            "user_profile":report_response.user_profile, 
                        }
                        
                        report_list.append(report_details)
              
                    details = {
                        "post_id" :post.post_id,
                        "user_id" :post.user_id,
                        "title" : post.title,
                        "content" :post.content,
                        "link" :post.link,
                        "date" :formatted_date,
                        "postimage" :post.postimage,
                        "profileimage":profile_response.profile_image if profile_response.profile_image else '',
                        "is_delete":post.is_delete if post.is_delete else False,
                        'like_count':post.like_count if post.like_count else 0,
                        'comment_count':post.comment_count if post.comment_count else 0,
                        "is_block":post.is_block if post.is_block else False,
                        "is_report":post.is_report if post.is_report else False,
                        "reports":report_list
                                             
                    }
                    post_details.append(details)   
                    
                    
                serializer = PostSerializers(post_details, many=True)
                if serializer.is_valid:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Data in not found", status=status.HTTP_404_NOT_FOUND)
                    
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
            
            
            
            
# Hide Post

class HidePost(APIView):
    def post(self, request):
    
        try:
            auth = authorization(request)
            if auth.admin:
                post_id = request.data.get('postId')
                response = client.hide_post(post_id)
                return Response(f"{response.message}", status=status.HTTP_200_OK)
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
                