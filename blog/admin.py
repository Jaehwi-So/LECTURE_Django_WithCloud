from django.contrib import admin

from .models import Post, Category, Tag

admin.site.register(Post)

#Admin 페이지에 카테고리의 슬러그를 이름과 일치시키게 하도록 추가
class AutoSlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, AutoSlugAdmin)


admin.site.register(Tag, AutoSlugAdmin)