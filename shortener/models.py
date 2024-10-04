# from django.db import models
# from django.utils.crypto import get_random_string

# class URL(models.Model):
#     original_url = models.URLField()
#     short_code = models.CharField(max_length=10, unique=True)

#     def save(self, *args, **kwargs):
#         if not self.short_code:
#             self.short_code = get_random_string(6)  # Generate a 6-character random code
#             print(f"Generated short code: {self.short_code}")  # Debugging line
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f'{self.original_url} -> {self.short_code}'
# ================================================================================
from django.db import models

class URL(models.Model):
    original_url = models.URLField(max_length=500)
    short_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.original_url
