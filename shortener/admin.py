from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db.models import Count, Sum
from django.urls import path
from django.template.response import TemplateResponse
from django.utils import timezone
from datetime import timedelta
from .models import URL, URLClick

# Custom Admin Site
class CustomAdminSite(admin.AdminSite):
    site_header = 'URL Shortener Administration'
    site_title = 'URL Shortener Admin'
    index_title = 'Dashboard'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        # Calculate statistics
        total_urls = URL.objects.count()
        total_clicks = URLClick.objects.count()
        total_users = User.objects.count()

        # Last 7 days data
        week_ago = timezone.now() - timedelta(days=7)
        recent_clicks = URLClick.objects.filter(clicked_at__gte=week_ago)

        # Top URLs
        top_urls = URL.objects.annotate(
            click_count=Count('clicks')
        ).order_by('-click_count')[:5]

        # Daily clicks for chart
        daily_clicks = []
        for i in range(7):
            day = timezone.now() - timedelta(days=6-i)
            clicks = URLClick.objects.filter(
                clicked_at__date=day.date()
            ).count()
            daily_clicks.append({
                'date': day.strftime('%a'),
                'clicks': clicks
            })

        # Device stats
        device_stats = URLClick.objects.values('device_type').annotate(
            count=Count('id')
        )

        context = dict(
            self.each_context(request),
            total_urls=total_urls,
            total_clicks=total_clicks,
            total_users=total_users,
            top_urls=top_urls,
            daily_clicks=daily_clicks,
            device_stats=device_stats,
        )
        return TemplateResponse(request, "admin/dashboard.html", context)

# Create custom admin site instance
admin_site = CustomAdminSite(name='custom_admin')

# URL Admin
@admin.register(URL, site=admin_site)
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
@admin.register(URLClick, site=admin_site)
class URLClickAdmin(admin.ModelAdmin):
    list_display = ('url', 'ip_address', 'country', 'device_type', 'clicked_at')
    list_filter = ('clicked_at', 'country', 'device_type')
    search_fields = ('ip_address', 'url__short_code')
    date_hierarchy = 'clicked_at'
    readonly_fields = ('url', 'ip_address', 'user_agent', 'referrer', 'country', 'city', 'device_type', 'clicked_at')

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'url_count', 'is_staff')

    def url_count(self, obj):
        return obj.url_set.count()
    url_count.short_description = 'URLs Created'

# Register models
admin_site.register(User, CustomUserAdmin)
