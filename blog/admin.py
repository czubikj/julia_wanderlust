from django.contrib import admin
from . import models

class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created',
        'updated',
        'author'
    )
    list_filter = (
        'status',
    )
    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )
    prepopulated_fields = {'slug': ('title',)}

class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)} #prepopulate with value in name

# Register all` models
admin.site.register(models.Post)
admin.site.register(models.Topic)

