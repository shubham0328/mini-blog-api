from rest_framework import serializers #-> convert to json(for api's)
from .models import Post, Comment


# efines how a Comment object is converted to JSON when sending it through API responses
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ["id", "text", "created_at"]
        read_only_fields = ["id", "created_at"]

# Defines how a Post object is converted to JSON
class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username') #author shows the username
    comments = CommentSerializer(many=True, read_only=True)  # nested comments

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "created_at", "comments"]
