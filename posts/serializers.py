from rest_framework import serializers
from .models import Category, Post, Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "author", "author_username", "text", "created_at"]
        read_only_fields = ["author", "created_at"]


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "author_username",
            "category",
            "category_name",
            "title",
            "slug",
            "content",
            "image",
            "is_published",
            "created_at",
            "updated_at",
            "comments",
        ]
        read_only_fields = ["author", "created_at", "updated_at"]

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError("Sarlavha kamida 5 ta belgidan iborat bo'lishi kerak.")
        return value

    def validate_content(self, value):
        if len(value) < 20:
            raise serializers.ValidationError("Maqola matni kamida 20 ta belgidan iborat bo'lishi kerak.")
        return value