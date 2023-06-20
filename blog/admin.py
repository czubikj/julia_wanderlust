from django.contrib import admin
from . import models

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = (
        'title',
        'created',
        'updated',
        'author',
    )
    list_filter = (
        'status',
        'topic',
    )
    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

class TopicAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # prepopulate with value in name
    list_display = (
        'name',
        'slug',
    )

# Register all` models
admin.site.register(models.Post)
admin.site.register(models.Topic)

