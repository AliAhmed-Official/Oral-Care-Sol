from django.contrib import admin
from userauths.models import User, Profile

class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'User_Email',
    ]

class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'full_name',
        'bio',
        'phone'
    ]

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)