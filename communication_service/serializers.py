from rest_framework import serializers




# Chat friends details serializer

class ChatUserSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    full_name = serializers.CharField(max_length = 50)
    user_profile = serializers.URLField(required=False, allow_blank=True)
    message = serializers.IntegerField()
    online = serializers.BooleanField()



# Notification serializer


class NotificationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    other_user_id = serializers.IntegerField()
    follower = serializers.IntegerField(required=False)
    post = serializers.IntegerField(required=False)
    content = serializers.CharField(max_length = 20)
    timestamp = serializers.CharField()
    read = serializers.BooleanField()
    full_name = serializers.CharField(max_length = 50)
    user_profile = serializers.URLField(required=False, allow_blank=True)