from rest_framework import serializers



# User List Serializer

class UserListSerializer(serializers.Serializer):
    id = serializers.CharField(max_length = 50)
    username = serializers.CharField(max_length = 50)
    full_name = serializers.CharField(max_length = 50)
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
    


# Chat user data



class UserDataSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField(max_length = 50)
    username = serializers.CharField(max_length = 50)
    user_profile = user_profile = serializers.URLField(required=False, allow_blank=True)
    
    


# User followers and Followings 


class UserFriendsSerializer(serializers.Serializer):
    follower = UserDataSerializer(many=True, required=False)
    followed = UserDataSerializer(many=True, required=False)
    
    



    
    


