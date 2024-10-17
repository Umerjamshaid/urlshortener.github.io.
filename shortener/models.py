from django.db import models
from django.utils.crypto import get_random_string
from django.db import models
from django.db import models
from django.contrib.auth.models import User 

class URL(models.Model):
    original_url = models.URLField(max_length=500)
    short_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.original_url
