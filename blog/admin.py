from django.contrib import admin
from .models import Article, Tag


class TagInline(admin.TabularInline):
    model = Tag


class ArticleAdmin(admin.ModelAdmin):
    """
    使用自定义管理页面来替代model自动生成的管理页面
    """
    model = Article
    inlines = [TagInline]
    fields = ['title', 'content']
    search_fields = ('title', 'content')
    list_display = ('title', 'content', 'pub_date')


# Register your models here.
admin.site.register(Article, ArticleAdmin)
