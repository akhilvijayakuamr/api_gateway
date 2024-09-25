from rest_framework import serializers




# Replies details serializer

class ReplaySerializer(serializers.Serializer):
    replay_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    mention_user_id = serializers.IntegerField()
    mention_user = serializers.CharField()
    content = serializers.CharField()
    date = serializers.DateTimeField()
    full_name = serializers.CharField()
    user_profile = serializers.URLField(required=False, allow_blank=True)


# Comment details serializer

class CommentSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    content = serializers.CharField()
    date = serializers.DateTimeField()
    full_name = serializers.CharField()
    user_profile = serializers.URLField(required=False, allow_blank=True)
    replies = ReplaySerializer(many=True, required=False)


#Post serializer

class PostSerializers(serializers.Serializer):
    post_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    title = serializers.CharField(max_length = 100)
    content = serializers.CharField()
    link = serializers.URLField(required = False, allow_blank=True)
    date = serializers.DateTimeField()
    postimage = serializers.URLField(required = False, allow_blank=True)
    profileimage = serializers.URLField(required = False, allow_blank=True)
    bio = serializers.CharField(required=False, allow_blank=True)
    full_name = serializers.CharField(required=False, allow_blank=True)
    username = serializers.CharField(required=False, allow_blank=True)
    like = serializers.BooleanField(required=False, default=False)
    like_count = serializers.IntegerField(required=False, default=0)
    comment_count = serializers.IntegerField(required=False, default=0)
    comments = CommentSerializer(many=True, required=False)
    