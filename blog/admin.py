from django.contrib import admin
from . import models
from .models import Comment

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        'title',
        'created',
        'updated',
        'author'
    )
    list_filter = (
        'status',
        'topics',
    )
    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )
    inlines = [
        CommentInline,
    ]
# Register all` models
admin.site.register(models.Post, PostAdmin)

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)} # prepopulate with value in name

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ( #list display for comments is customized
        'name',
        'email',
        'created',
        'approved', #approved checkbox
    )
    list_filter = ( #list display for comments is filterable by which records are approved
        'approved',
    )
    search_fields = ( #list display for comments is searchable
        'name', #by commenter's name
        'text', #by comment text
        'email', #by commenter's email
    )
    actions = (
        'approve_comments'
    )

    def approve_comments(self, queryset):
        queryset.update(approved=True)

