from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Community(models.Model):
    """Model representing a community."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, null=True, blank=True)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Confession(models.Model):
    """Model representing a user confession with optional anonymity."""
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Optional for anonymous
    community = models.ForeignKey(Community, on_delete=models.CASCADE, null=True, blank=True, related_name='confessions')

    def __str__(self):
        return self.content[:50]

class Comment(models.Model):
    confession = models.ForeignKey(Confession, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content[:50]
