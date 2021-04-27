from django.db import models
from django.utils.timezone import now
from datetime import timedelta
from multiselectfield import MultiSelectField

"""
Model Class For Posts
"""


class Post(models.Model):
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
    # MultiselectField to allow user to have many topics for a single post
    post_topic = MultiSelectField(
        choices=TOPICS,
        max_choices=4,
        max_length=7)

    created_on = models.DateTimeField(auto_now_add=True)

    post_message = models.TextField()
    # expiration time is current time + 5 minutes
    post_expiration = models.DateTimeField(
        default=now() + timedelta(minutes=5))

    post_status = models.CharField(
        choices=STATUS,
        default=LIVE,
        max_length=1)

    owner = models.ForeignKey(
        'auth.User',
        related_name='posts',
        on_delete=models.CASCADE)

    """
    model function checks if the post is expired
    and changes the post_status accordingly. 
    """
    # Model function to check if post is expired and set the status accordingly.

    def post_expired(self):
        time = now()
        if time > self.post_expiration:
            self.post_status = self.EXPIRED
            self.save()
            return True
        return False


"""
Model class for LikeDislike interactions
"""


class LikeDislike(models.Model):
    LIKE, DISLIKE, = 'L', 'D'
    INTERACTION = [
        (LIKE, 'Like'),
        (DISLIKE, 'Dislike')
    ]

    """
    Model Fields
    """
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
        max_length=1)
    created_on = models.DateTimeField(auto_now_add=True)


"""
Model class for Comment interaction
"""


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
