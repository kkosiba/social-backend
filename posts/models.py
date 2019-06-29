from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete

User = get_user_model()


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)
    likes_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return (
            str(self.pk)
            + ": "
            + str(self.user.first_name)
            + " "
            + str(self.user.last_name)
        )


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField(max_length=250, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} said '{self.content}'"


# Signals
def inc_comment_count(sender, instance, **kwargs):
    """Increment the number of comments for a given post once user
    submits a comment"""

    post = instance.post
    post.comments_count += 1
    post.save()


def dec_comment_count(sender, instance, **kwargs):
    """Decrement the number of comments for a given post once 
    a comment is deleted"""

    post = instance.post
    post.comments_count -= 1
    post.save()


post_save.connect(inc_comment_count, sender=Comment)
post_delete.connect(dec_comment_count, sender=Comment)
