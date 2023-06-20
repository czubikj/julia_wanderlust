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

# Register the `Post` model
admin.site.register(models.Post)

@admin.register(models.Topic) #convenient decorator used instead of admin.site.register`
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)} #prepopulate with value in name