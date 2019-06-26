from django.db import models
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField(max_length=250, blank=False, null=False)
    created_at = models.DateTimeField(auto_now=True)
