from django.shortcuts import get_object_or_404
from rest_framework import generics, mixins, filters
from rest_framework import permissions
from posts.models import Post, Comment
from .serializers import (
    PostListCreate,
    PostRetrieveUpdateDelete,
    CommentListCreate,
    CommentRetrieveUpdateDelete,
)
from .permissions import IsOwner


class PostListCreate(mixins.CreateModelMixin, generics.ListAPIView):
    """
    This API view provides `list` and `create` actions for posts.
    Unrestricted GET requests and authenticated POST requests only.
    """

    queryset = Post.objects.order_by("pk")
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PostListCreate

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostRetrieveUpdateDelete(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView
):
    """
    This API view provides `retrieve`, `update` and `destroy` actions for posts.
    Unrestricted GET requests and authenticated (with object permissions)
    PUT/DELETE requests only.
    """

    queryset = Post.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)
    serializer_class = PostRetrieveUpdateDelete
    lookup_url_kwarg = "post_pk"

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class CommentListCreate(mixins.CreateModelMixin, generics.ListAPIView):
    """
    This API view provides `list` and `create` actions for comments.
    Unrestricted GET requests and authenticated POST requests only.
    """

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs.get("post_pk"))

    def get_serializer_context(self):
        return {
            **self.get_renderer_context(),
            **{"post_pk": self.kwargs.get("post_pk")},
        }

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = CommentListCreate
    lookup_url_kwarg = "post_pk"

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class CommentRetrieveUpdateDelete(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.RetrieveAPIView
):
    """
    This API view provides `retrieve`, `update` and `destroy` actions for comments.
    Unrestricted GET requests and authenticated (with object permissions)
    PUT/DELETE requests only.
    """

    def get_object(self):
        post_pk = self.kwargs.get("post_pk")
        comment_pk = self.kwargs.get("comment_pk")
        return get_object_or_404(Comment, pk=comment_pk, post=post_pk)

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)
    serializer_class = CommentRetrieveUpdateDelete

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
