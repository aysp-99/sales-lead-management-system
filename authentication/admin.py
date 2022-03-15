from django.contrib import admin
from authentication.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'phonenumber')


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.site_header = "Leads Management Platform"
admin.site.site_title = "Leads Management Admin Site"
admin.site.index_title = "Leads Management Admin"
