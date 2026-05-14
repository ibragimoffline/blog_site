from rest_framework import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Post, Comment
from .serializers import CategorySerializer, PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, IsCommentAuthorOrReadOnly, IsAdminOrReadOnly
# Create your views here.


class CategoryListCreateAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        self.check_permissions(request)
        serializer = CategorySerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)

        if category is None:
            return Response(
                {"error": "Kategoriya topilmadi"},
                status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        self.check_permissions(request)

        category = self.get_object(pk)

        if category is None:
            return Response(
                {"error": "Kategoriya topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(category, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        self.check_permissions(request)

        category = self.get_object(pk)

        if category is None:
            return Response(
                {"error": "Kategoriya topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = CategorySerializer(
            category,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.check_permissions(request)

        category = self.get_object(pk)

        if category is None:
            return Response(
                {"error": "Kategoriya topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )

        category.delete()

        return Response(
            {"message": "Kategoriya o'chirildi"},
            status=status.HTTP_204_NO_CONTENT
        )


class PostListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.filter(is_published=True).order_by("-created_at")
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return None

    def get(self, request, pk):
        post = self.get_object(pk)

        if post is None:
            return Response(
                {"error": "Post topilmadi"},
                status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        post = self.get_object(pk)

        if post is None:
            return Response(
                {"error": "Post topilmadi"},
                status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, post)

        serializer = PostSerializer(post, data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        post = self.get_object(pk)

        if post is None:
            return Response(
                {"error": "Post topilmadi"},
                status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, post)

        serializer = PostSerializer(
            post,
            data=request.data,
            partial=True)

        if serializer.is_valid():
            serializer.save(author=request.user)

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        post = self.get_object(pk)

        if post is None:
            return Response(
                {"error": "Post topilmadi"},
                status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, post)
        post.delete()
        return Response(
            {"message": "Post o'chirildi"},
            status=status.HTTP_204_NO_CONTENT)


class CommentListCreateAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        comments = Comment.objects.all().order_by("-created_at")
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsCommentAuthorOrReadOnly]

    def get_object(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            return None

    def get(self, request, pk):
        comment = self.get_object(pk)

        if comment is None:
            return Response(
                {"error": "Comment topilmadi"},
                status=status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        comment = self.get_object(pk)

        if comment is None:
            return Response(
                {"error": "Comment topilmadi"},
                status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, comment)

        serializer = CommentSerializer(comment, data=request.data)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        comment = self.get_object(pk)

        if comment is None:
            return Response(
                {"error": "Comment topilmadi"},
                status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(
            comment,
            data=request.data,
            partial=True)

        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_object(pk)

        if comment is None:
            return Response(
                {"error": "Comment topilmadi"},
                status=status.HTTP_404_NOT_FOUND)

        self.check_object_permissions(request, comment)

        comment.delete()
        return Response(
            {"message": "Comment o'chirildi"},
            status=status.HTTP_204_NO_CONTENT)
