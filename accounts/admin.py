from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "hash_algorithm", "password_hash", "created_at")
    list_filter = ("hash_algorithm",)
    search_fields = ("username",)
