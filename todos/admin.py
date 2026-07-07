from django.contrib import admin
from .models import Todo, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "color")


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "category", "priority", "due_date", "completed")
    list_filter = ("completed", "priority", "category", "owner")
    search_fields = ("title",)