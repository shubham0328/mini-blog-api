from django.db import models
from django.contrib.auth.models import User

# This replaces POSTS & COMMENTS lists.
# IDs are auto-generated, no need for _next_post_id or _next_comment_id
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=2000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # link to built-in User
    created_at = models.DateTimeField(auto_now_add=True)        # timestamp auto-generated

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.post}"
