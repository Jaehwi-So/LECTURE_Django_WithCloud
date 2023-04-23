from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Post, Category, Tag, Comment, Test

# Register your models here.

admin.site.register(Post, MarkdownxModelAdmin)

class AutoSlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, AutoSlugAdmin)
admin.site.register(Tag, AutoSlugAdmin)
admin.site.register(Comment)
admin.site.register(Test)