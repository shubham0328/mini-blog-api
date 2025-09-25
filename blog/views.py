from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer




@api_view(['POST'])
@permission_classes([AllowAny])  # signup is open
def signup(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response({"error": "username and password required"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "username already exists"}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


# Helper function for safely reading query params (page, page_size)
def _parse_positive_int(value, default):
    """
    Safely parse a positive integer from string-like 'value'.
    Return (int_value, None) on success, or (None, error_message) on failure.
    """
    if value is None:
        return default, None
    try:
        iv = int(value)
    except (ValueError, TypeError):
        return None, "must be an integer"
    if iv <= 0:
        return None, "must be a positive integer"
    return iv, None


# Posts list & create post
class PostListCreate(APIView):
    """
    GET: list posts (latest first), supports pagination ?page=&page_size=
    POST: create post (auth required)
    """
    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]   # POST requires login
        return [AllowAny()]              # GET is public

    
    # Lists all posts latest first (-id)
    # Supports pagination using query params: ?page=2&page_size=5
    # Converts posts to JSON using PostSerializer
    def get(self, request):
        page, err = _parse_positive_int(request.GET.get("page"), 1)
        if err:
            return Response({"page": f"page {err}"}, status=status.HTTP_400_BAD_REQUEST)

        page_size, err = _parse_positive_int(request.GET.get("page_size"), 5)
        if err:
            return Response({"page_size": f"page_size {err}"}, status=status.HTTP_400_BAD_REQUEST)

        posts = Post.objects.all().order_by("-id")  # latest first
        start = (page - 1) * page_size
        end = start + page_size
        serializer = PostSerializer(posts[start:end], many=True)
        return Response(serializer.data)
    


    # Creates a new post from incoming JSON & Validate data 
    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)  # logged-in user becomes author
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Single post detail (GET, PUT/PATCH, DELETE)
#This handles retrieving GET, Updating PUT, and deleting DELETE a single post with its comments
class PostDetail(APIView):
    """
    GET/PUT/DELETE: return single post with its comments (public)
    """
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return Response(serializer.data)


    #Update and delete actions are restricted to the post’s author, while anyone can view the post
    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        if post.author != request.user:
            raise PermissionDenied("You cannot update this post.")

        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        if post.author != request.user:
            raise PermissionDenied("You cannot delete this post.")

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# It allows a logged-in user to add a comment to a specific post
# It ensures the post exists and saves the comment with the current user as the author
class CommentCreate(APIView):
    """
    POST: add a comment to a specific post (auth required)
    """
    permission_classes = [IsAuthenticated]  # must be logged in

    def post(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({"detail": "Post not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, post=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# allows a logged-in user to update or delete comment 
# It ensures the comment exists or not & author-only permissions
class CommentDetail(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        if comment.author != request.user:
            raise PermissionDenied("You cannot update this comment.")

        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            comment = Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        if comment.author != request.user:
            raise PermissionDenied("You cannot delete this comment.")

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)