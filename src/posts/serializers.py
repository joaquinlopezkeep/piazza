from django.db.models import fields
from .models import Post, LikeDislike, Comment
from rest_framework import serializers, fields
from rest_framework.validators import UniqueTogetherValidator


class PostSerializer(serializers.ModelSerializer):
    post_topic = fields.MultipleChoiceField(choices=Post.TOPICS)
    post_owner = serializers.ReadOnlyField(source='post_owner.username')
    likes = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True)
    comments = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True)

    class Meta:
        model = Post
        fields = [
            'id',
            'post_title',
            'post_topic',
            'created_on',
            'post_message',
            'post_expiration',
            'post_status',
            'post_owner',
            'likes',
            'comments']
        extra_kwargs = {
            'post_expiration': {'read_only': True},
            'post_status': {'read_only': True}
        }


class LikeDislikeSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Post.objects.all())

    class Meta:
        model = LikeDislike
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=LikeDislike.objects.all(),
                fields=['owner', 'post'],
                message='You cannot interact with this post more than once, to change your interactions use a PUT request.'
            )
        ]

    def validate_post(self, value):
        if value.post_expired():
            raise serializers.ValidationError('This post has expired')
        return value

    def create(self, validated_data):
        LikeDislike = LikeDislike(
            owner=self.context['request'].user,
            post=validated_data['post']
        )
        LikeDislike.save()
        return LikeDislike


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault())
    post = serializers.PrimaryKeyRelatedField(
        many=False, queryset=Post.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'

    def validate_post(self, value):
        if value.post_expired():
            raise serializers.ValidationError('This post has expired')
        return value

    def create(self, validated_data):
        comment = Comment(
            owner=self.context['request'].user,
            post=validated_data['post'],
            comment=validated_data['comment']
        )
        comment.save()
        return comment
