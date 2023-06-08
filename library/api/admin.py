from django.contrib import admin

# Register your models here.
from api.models import Book, Author, Category


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'id')
    list_display = ('title', 'id')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ('name', 'id')
    list_display = ('name', 'id')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('title', 'id')
    list_display = ('title', 'id')
