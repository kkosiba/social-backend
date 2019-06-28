from rest_framework import viewsets, mixins, filters
from rest_framework import permissions
from posts.models import Post
from .serializers import PostListDetail, PostCreateUpdate
from .permissions import IsOwner

class PostViewSet(viewsets.ModelViewSet):
    """
    This viewset provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for posts.
    """

    queryset = Post.objects.order_by("pk")
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner)

    filter_backends = (filters.SearchFilter,)
    search_fields = ("content",)

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return PostCreateUpdate
        else:
            return PostListDetail

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
