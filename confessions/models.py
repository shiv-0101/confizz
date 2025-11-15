from django.db import models
from django.contrib.auth.models import User

class Confession(models.Model):
    """Model representing a user confession with optional anonymity."""
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional for anonymous

    def __str__(self):
        return self.content[:50]

class Comment(models.Model):
    confession = models.ForeignKey(Confession, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content[:50]
