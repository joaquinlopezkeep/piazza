
from django.db.models import Count
# local imports
from .serializers import PostSerializer, LikeDislikeSerializer, CommentSerializer
from .models import Post, LikeDislike, Comment
# rest framework imports
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDislikeViewSet(viewsets.ModelViewSet):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# filter posts by topic and status


def filter_by_topic_status(topic, status):
    qs = filter_by_topic(topic)
    if status is not None:
        qs = qs.filter(post_status=status.upper())
        return qs
    return qs

# filter posts by topic


def filter_by_topic(topic):
    qs = Post.objects.all()
    if topic is not None:
        qs = qs.filter(post_topic__contains=topic.upper())
        return qs
    return qs

# return posts by topic and status


@api_view(['GET'])
def post_by_topic_status(request, topic, status):
    qs = filter_by_topic_status(topic, status)
    serializers = PostSerializer(qs, many=True)
    print(serializers.data)
    return Response(serializers.data)

# return posts by topic


@api_view(['GET'])
def all_by_topic(request, topic):
    qs = filter_by_topic(topic)
    serializers = PostSerializer(qs, many=True)
    print(serializers.data)
    return Response(serializers.data)

# return the single most active post by topic


@api_view(['GET'])
def most_active_topic(request, topic):
    posts = filter_by_topic(topic).annotate(
        Count('likes')).order_by('-likes__count').first()
    serializer = PostSerializer(posts)
    return Response(serializer.data)

# return the single most active post by topic and status


@api_view(['GET'])
def most_active_topic_status(request, topic, status):
    posts = filter_by_topic_status(topic, status).annotate(
        Count('likes')).order_by('-likes__count').first()
    serializer = PostSerializer(posts)
    return Response(serializer.data)
