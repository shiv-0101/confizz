from django.contrib import admin
from .models import Confession

@admin.register(Confession)
class ConfessionAdmin(admin.ModelAdmin):
    """Admin view for the Confession model."""
    list_display = ('id', 'content_snippet', 'created_at', 'upvotes')
    list_filter = ('created_at',)
    search_fields = ('content',)
    ordering = ('-created_at',)

    def content_snippet(self, obj):
        """Returns a short snippet of the confession content for the list view."""
        return obj.content[:75] + '...' if len(obj.content) > 75 else obj.content
    content_snippet.short_description = 'Content Snippet'