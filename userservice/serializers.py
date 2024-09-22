from rest_framework import serializers

class UserListSerializer(serializers.Serializer):
    id = serializers.CharField(max_length = 50)
    username = serializers.CharField(max_length = 50)
    full_name = serializers.CharField(max_length = 50)
    email = serializers.EmailField()
    is_active = serializers.BooleanField()
    
    


