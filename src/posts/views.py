
from django.db.models import Count
# local imports
from .serializers import PostSerializer, LikeDislikeSerializer, CommentSerializer
from .models import Post, LikeDislike, Comment
# rest framework imports
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['post_topic']

    @action(detail=False, methods=['get'])
    def most_active(self, request):
        posts = Post.objects.annotate(Count('likes')).order_by('-likes__count')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(post_owner=self.request.user)


class LikeDislikeViewSet(viewsets.ModelViewSet):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
