from django.urls import path #path -> django function that maps URL pattern to a view
from .views import signup, PostListCreate, PostDetail, CommentCreate, CommentDetail
#PostListCreate -> handles listing posts (GET) & creating posts (POST)
#PostDetail -> Fetch single post by its ID
#CommentCreate -> Adding a comment to specific post


urlpatterns = [     #Looks which URL maps to which view
    path("signup/", signup),
    path("posts/", PostListCreate.as_view(), name="post-list-create"),
    path("posts/<int:pk>/", PostDetail.as_view(), name="post-detail"),
    path("posts/<int:pk>/comments/", CommentCreate.as_view(), name="post-comments"),
    path("comments/<int:pk>/", CommentDetail.as_view(), name="comment-detail"),
]
