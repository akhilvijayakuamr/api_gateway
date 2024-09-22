from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from grpc import RpcError
from api_gateway.auth import authorization
from .service import APIPostClient
from userservice.service import APIUserClient
from . serilizers import PostSerializers
from datetime import datetime

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
        except authorization:
            return Response({'error':'Autharization Denied'}, status=status.HTTP_401_UNAUTHORIZED)
        
        




# Get all post



class GetAllPost(APIView):
    def post(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                user_id = request.data.get('userId')
                
                response = client.get_all_posts(user_id)
                
                all_posts = response.posts
                print(all_posts)
                
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
                        "like":post.like if post.like else False                     
                    }
                    
                    
                    
                    post_details.append(details)
                    
                print("post_details", post_details)
                    
                    
                
                serializer = PostSerializers(post_details, many=True)
                if serializer.is_valid:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response("Data in not found", status=status.HTTP_404_NOT_FOUND)
                    
        except RpcError as e:
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
                    
                    
                    details = {
                        "comment_id":comment.comment_id,
                        "user_id":comment.user_id,
                        "content":comment.content,
                        "date":comment_formatted_date,
                        "full_name":comment_response.full_name,
                        "user_profile":comment_response.user_profile,  
                    }
                    
                    comment_list.append(details)
                    
                    
              
                    
                
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
                    'comments': comment_list,
                    
                }
                
                serializer = PostSerializers(data=data)
                print("Is serializer valid:", serializer.is_valid())
                print("Serializer errors:", serializer.errors)
                
                if serializer.is_valid:
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    print("working not")
                    return Response("Data in not found", status=status.HTTP_404_NOT_FOUND)
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
            
            
            
            
# Like post


class LikeApiView(APIView):
    def post(self, request):
        try:
            auth = authorization(request)
            if auth.user:
                post_id = request.data.get('postId')
                user_id = request.data.get('userId')
                response = client.like_post(int(post_id), int(user_id))
                return Response(f"{response.message}", status=status.HTTP_201_CREATED)
        except RpcError as e:
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
        print("it is working")
        try:
            auth = authorization(request)
            if auth.user:
                post_id = request.data.get('postId')
                user_id = request.data.get('userId')
                content = request.data.get('content')
                response = client.comment_post(int(post_id), int(user_id), content)
                print(response)
                return Response(f"{response.message}", status=status.HTTP_201_CREATED)
        except RpcError as e:
            return Response({
                "error": f"{e.details()}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
        except Exception as e:
            return Response({
                "error": f"An unexpected error occurred: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
            
            
            
            


                