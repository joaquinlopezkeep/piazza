from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from multiselectfield import MultiSelectField


class Post(models.Model):
    """
    Model Class For Posts
    """
    POLITICS, HEALTH, TECHNOLOGY, SPORT = 'P', 'H', 'T', 'S'
    LIVE, EXPIRED = 'L', 'E'
    TOPICS = [
        (POLITICS, 'Politics'),
        (HEALTH, 'Health'),
        (TECHNOLOGY, 'Technology'),
        (SPORT, 'Sport'),
    ]

    STATUS = [
        (LIVE, 'Live'),
        (EXPIRED, 'Expired')
    ]

    """
    Model Fields
    """
    post_title = models.CharField(max_length=100)

    post_topic = MultiSelectField(
        choices=TOPICS,
        max_choices=4,
        max_length=7)

    created_on = models.DateTimeField(auto_now_add=True)

    post_message = models.TextField()

    post_expiration = models.DateTimeField(
        default=now() + timedelta(minutes=5))

    post_status = models.CharField(
        choices=STATUS,
        default=LIVE,
        max_length=1)

    post_owner = models.ForeignKey(
        'auth.User',
        related_name='posts',
        on_delete=models.CASCADE)

    def post_expired(self):
        time = now()
        if time > self.post_expiration:
            self.post_status = self.EXPIRED
            self.save()
            return True
        return False


class LikeDislike(models.Model):
    UNSET, LIKE, DISLIKE, = 'U', 'L', 'D'
    INTERACTION = [
        (UNSET, 'Unset'),
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    ]

    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='likes')
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='likes')
    interaction = models.CharField(
        choices=INTERACTION,
        default=UNSET,
        max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name='comments')
    owner = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='comments')
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
