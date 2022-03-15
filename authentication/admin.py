from django.contrib import admin
from authentication.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'phonenumber')


admin.site.register(UserProfile, UserProfileAdmin)
