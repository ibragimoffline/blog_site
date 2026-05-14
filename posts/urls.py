from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, PostViewSet, CommentViewSet
from .views import CategoryListCreateAPIView, CategoryDetailAPIView, PostListCreateAPIView, PostDetailAPIView, CommentListCreateAPIView, CommentDetailAPIView


router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("posts", PostViewSet, basename="post")
router.register("comments", CommentViewSet, basename="comment")


urlpatterns = [
    path("categories/", CategoryListCreateAPIView.as_view(), name="category-list-create"),
    path("categories/<int:pk>/", CategoryDetailAPIView.as_view(), name="category-detail"),
    path("posts/", PostListCreateAPIView.as_view(), name="post-list-create"),
    path("posts/<int:pk>/", PostDetailAPIView.as_view(), name="post-detail"),
    path("comments/", CommentListCreateAPIView.as_view(), name="comment-list-create"),
    path("comments/<int:pk>/", CommentDetailAPIView.as_view(), name="comment-detail"),
]
