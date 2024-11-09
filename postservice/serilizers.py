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
    comment_id = serializers.IntegerField(required=False)


# Comment details serializer

class CommentSerializer(serializers.Serializer):
    comment_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    content = serializers.CharField()
    date = serializers.DateTimeField()
    full_name = serializers.CharField()
    user_profile = serializers.URLField(required=False, allow_blank=True)
    reply_count = serializers.IntegerField(required=False)
    replies = ReplaySerializer(many=True, required=False)


# Report Details serializer

class ReportSerializer(serializers.Serializer):
    report_id = serializers.IntegerField()
    report_user_id = serializers.IntegerField()
    reson =  serializers.CharField()
    date = serializers.DateTimeField()
    full_name = serializers.CharField()
    user_profile = serializers.URLField(required=False, allow_blank=True)
    
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
    is_delete = serializers.BooleanField(required=False, default=False)
    like_count = serializers.IntegerField(required=False, default=0)
    comment_count = serializers.IntegerField(required=False, default=0)
    is_block = serializers.BooleanField(required=False, default=False)
    is_report = serializers.BooleanField(required=False, default=False)
    comments = CommentSerializer(many=True, required=False)
    reports = ReportSerializer(many=True, required=False)
    