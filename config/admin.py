from django.contrib import admin
from axes.models import AccessAttempt

@admin.register(AccessAttempt)
class AccessAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'ip_address', 'attempt_time', 'user_agent', 'path_info')
    search_fields = ('username', 'ip_address')
