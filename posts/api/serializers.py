from django.contrib.auth import get_user_model
from rest_framework import serializers
from posts.models import Post


class AuthorListingField(serializers.RelatedField):
    def to_representation(self, value):
        return f"{value.first_name.capitalize()} {value.last_name.capitalize()}"

    def to_internal_value(self, value):
        return value


class PostListDetail(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="post-detail", lookup_field="pk"
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


class PostCreateUpdate(serializers.ModelSerializer):
    user = AuthorListingField(queryset=get_user_model().objects.all())
    created_at = serializers.DateTimeField(format="%a, %d %b  %I:%M %p", read_only=True)

    class Meta:
        model = Post
        fields = PostListDetail.Meta.fields
        read_only_fields = ["user", "likes_count", "comments_count", ]

    def create(self, validated_data):
        validated_data["likes_count"] = 0
        validated_data["comments_count"] = 0
        return Post.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.user = validated_data.get("user", instance.user)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance
