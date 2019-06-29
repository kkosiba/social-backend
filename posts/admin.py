from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment

    def get_extra(self, request, obj=None, **kwargs):
        return 1

    fieldsets = (
        (None, {
            "fields": ("user", "content",)
        }),
    )


class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]
    fieldsets = (
        (None, {
            "fields": ("user", "content",)
        }),
    )

    list_display = ("user", "created_at", "likes_count", "comments_count",)
    list_filter = ("likes_count", "comments_count",)
    



# Register your models here.
admin.site.register(Post, PostAdmin)
