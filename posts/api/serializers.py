from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import serializers
from posts.models import Post, Comment


class AuthorListingField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.first_name.capitalize()} {value.last_name.capitalize()}"

    def to_internal_value(self, value):
        return value


class CommentListCreate(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = AuthorListingField(queryset=get_user_model().objects.all())
    created_at = serializers.DateTimeField(format="%a, %d %b  %I:%M %p", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "content", "created_at"]
        read_only_fields = ["user"]

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        validated_data["post"] = Post.objects.filter(
            pk=self.context.get("post_pk")
        ).first()
        return Comment.objects.create(**validated_data)


class CommentRetrieveUpdateDelete(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = AuthorListingField(queryset=get_user_model().objects.all())
    created_at = serializers.DateTimeField(format="%a, %d %b  %I:%M %p", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "user", "post", "content", "created_at"]
        read_only_fields = ["user", "post"]

    def update(self, instance, validated_data):
        instance.user = self.context.get("request").user
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance


class PostListCreate(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="post-retrieve-update-delete", lookup_url_kwarg="post_pk"
    )
    user = AuthorListingField(queryset=get_user_model().objects.all())
    created_at = serializers.DateTimeField(format="%a, %d %b  %I:%M %p", read_only=True)

    class Meta:
        model = Post
        fields = [
            "url",
            "user",
            "content",
            "created_at",
            "likes_count",
            "comments_count",
        ]
        read_only_fields = ["user", "likes_count", "comments_count"]

    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        validated_data["likes_count"] = 0
        validated_data["comments_count"] = 0
        return Post.objects.create(**validated_data)


class PostRetrieveUpdateDelete(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="post-retrieve-update-delete", lookup_url_kwarg="post_pk"
    )
    user = AuthorListingField(queryset=get_user_model().objects.all())
    created_at = serializers.DateTimeField(format="%a, %d %b  %I:%M %p", read_only=True)
    comments = CommentListCreate(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ["url", "user", "content", "created_at", "comments"]

    def update(self, instance, validated_data):
        instance.user = self.context.get("request").user
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance
