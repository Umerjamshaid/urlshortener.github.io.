from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db.models import Count
from .models import URL, URLClick

# URL Admin
@admin.register(URL)
class URLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'original_url', 'user', 'click_count', 'created_at', 'status_badge')
    list_filter = ('created_at', 'user')
    search_fields = ('short_code', 'original_url', 'user__username')
    readonly_fields = ('short_code', 'created_at', 'click_count')
    date_hierarchy = 'created_at'

    def click_count(self, obj):
        return obj.clicks.count()
    click_count.short_description = 'Total Clicks'

    def status_badge(self, obj):
        if obj.clicks.count() > 100:
            color = 'green'
            text = 'Popular'
        elif obj.clicks.count() > 50:
            color = 'orange'
            text = 'Active'
        else:
            color = 'gray'
            text = 'New'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            color, text
        )
    status_badge.short_description = 'Status'

# Click Tracking Admin
@admin.register(URLClick)
class URLClickAdmin(admin.ModelAdmin):
    list_display = ('url', 'ip_address', 'country', 'device_type', 'clicked_at')
    list_filter = ('clicked_at', 'country', 'device_type')
    search_fields = ('ip_address', 'url__short_code')
    date_hierarchy = 'clicked_at'
    readonly_fields = ('url', 'ip_address', 'user_agent', 'referrer', 'country', 'city', 'device_type', 'clicked_at')

# Download Task Admin
from .models import DownloadTask
try:
    @admin.register(DownloadTask)
    class DownloadTaskAdmin(admin.ModelAdmin):
        list_display = ('task_id', 'video_url', 'status', 'progress', 'created_at')
        list_filter = ('status', 'created_at')
        search_fields = ('task_id', 'video_url')
        readonly_fields = ('task_id', 'created_at', 'completed_at')
except:
    pass  # DownloadTask model might not exist yet
