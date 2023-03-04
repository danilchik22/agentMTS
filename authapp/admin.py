from django.contrib import admin
from authapp.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "is_staff", "date_joined"]
    list_filter = ["is_staff"]
