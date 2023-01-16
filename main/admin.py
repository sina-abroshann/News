from django.contrib import admin
from .models import Category, News, Comment
from .models import Contact

admin.site.register(Category)


class AdminNews(admin.ModelAdmin):
    list_display = ('title', 'category', 'add_time')


admin.site.register(News, AdminNews)


class AdminComment(admin.ModelAdmin):
    list_display = ('news', 'email', 'comment', 'status')


admin.site.register(Comment, AdminComment)


class AdminContact(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'message')

admin.site.register(Contact, AdminContact)