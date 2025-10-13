from django.db import models
from django.utils.crypto import get_random_string
from django.contrib.auth.models import User

class URL(models.Model):
    original_url = models.URLField(max_length=500)
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Shortened URL'
        verbose_name_plural = 'Shortened URLs'

    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:50]}"

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = get_random_string(6)
        super().save(*args, **kwargs)

class URLClick(models.Model):
    url = models.ForeignKey(URL, on_delete=models.CASCADE, related_name='clicks')
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    referrer = models.URLField(max_length=2048, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    device_type = models.CharField(max_length=50, blank=True)
    clicked_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-clicked_at']
        verbose_name = 'URL Click'
        verbose_name_plural = 'URL Clicks'

    def __str__(self):
        return f"{self.url.short_code} - {self.clicked_at}"

class DownloadTask(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('downloading', 'Downloading'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    task_id = models.CharField(max_length=100, unique=True)
    video_url = models.URLField()
    format_id = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress = models.IntegerField(default=0)
    filename = models.CharField(max_length=500, blank=True)
    file_size = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Download Task'
        verbose_name_plural = 'Download Tasks'

    def __str__(self):
        return f"{self.task_id} - {self.status}"
