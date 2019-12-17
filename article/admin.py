from django.contrib import admin
from . import models

@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):   
    list_display = ["title", "author", "created_date"]
    list_filter = ["created_date"]
    search_fields = ["title"]

    class Meta: 
        model = models.Article

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):  
    list_display = ["comment_author","article","comment_date"] 
    list_filter = ["article"]
    search_fields = ["comment_author"]

    class Meta:
        model = models.Comment
