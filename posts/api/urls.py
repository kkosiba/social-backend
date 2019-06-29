from django.urls import path, include
from posts.api import views


urlpatterns = [
    path("", views.PostListCreate.as_view(), name="post-list"),
    path(
        "<int:post_pk>/",
        views.PostRetrieveUpdateDelete.as_view(),
        name="post-retrieve-update-delete",
    ),
    path("<int:post_pk>/comments/", views.CommentListCreate.as_view(), name="comment-list"),
    path(
        "<int:post_pk>/comments/<int:comment_pk>/",
        views.CommentRetrieveUpdateDelete.as_view(),
        name="comment-retrieve-update-delete",
    ),
]
