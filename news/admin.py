from django.contrib import admin
from .models import Category, Post, Author, Comment, PostCategory

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'categoryType', 'dateCreation', 'rating', 'author')
    list_filter = ('categoryType', 'dateCreation', 'postCategory')
    search_fields = ('title', 'text')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')
    search_filter = ('authorUser_username',)

class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentPost', 'commentUser', 'dateCreation', 'rating')
    list_filter = ('dateCreation', 'rating')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(PostCategory)

# Register your models here.
