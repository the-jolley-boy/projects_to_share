from django.contrib import admin
from blog.models import Post, Category, Comment

class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "created_on"]

    # def __str__(self):
    #     return self.title
    pass

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    pass

class CommentAdmin(admin.ModelAdmin):
    list_display = ["author", "created_on"]
    pass

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)