from django.contrib import admin
from authentication.models import UserProfile
from django.contrib import messages
from django.utils.translation import ngettext


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'email', 'phonenumber')
    actions = ['approve_sales_representative']

    @admin.action(description='Approve selected user as sales representative')
    def approve_sales_representative(self, request, queryset):
        updated = queryset.update(approval_status_pending=False)
        self.message_user(request, ngettext(
            '%d user was successfully approved as sales representative.',
            '%d users were successfully approved as sales representatives.',
            updated,
        ) % updated, messages.SUCCESS)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.site_header = "Leads Management Platform"
admin.site.site_title = "Leads Management Admin Site"
admin.site.index_title = "Leads Management Admin"
