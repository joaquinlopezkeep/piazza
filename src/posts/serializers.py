from django.db.models import fields
from .models import Post, LikeDislike, Comment
from rest_framework import serializers, fields
from rest_framework.validators import UniqueTogetherValidator

"""
Serializer for Post model
"""


class PostSerializer(serializers.ModelSerializer):
    post_topic = fields.MultipleChoiceField(choices=Post.TOPICS)
    owner = serializers.ReadOnlyField(source='owner.username')
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
            'owner',
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
        # A check to make sure a user cannot like a post multiple times
        # or like their own post.
        validators = [
            UniqueTogetherValidator(
                queryset=LikeDislike.objects.all(),
                fields=['owner', 'post'],
                message='You cannot interact with this post more than once, to change your interactions use a PUT request.'
            )
        ]

    # A check to make sure a user doesn't interact with an expired post.
    def validate_post(self, value):
        user = self.context['request'].user
        if value.owner == user:
            raise serializers.ValidationError('You can not like your own post')
        if value.post_expired():
            raise serializers.ValidationError('This post has expired')
        return value

    # The create function is primarily used to set the user using context.
    # setting the user like postserializer does gives an error NULL error as the user
    # is not yet set.
    def create(self, validated_data):
        like_dislike = LikeDislike(
            owner=self.context['request'].user,
            post=validated_data['post'],
            interaction=validated_data['interaction']
        )
        like_dislike.save()
        return like_dislike


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
