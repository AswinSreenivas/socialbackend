from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class Platform(models.TextChoices):
    FACEBOOK = 'facebook'
    INSTAGRAM = 'instagram'


class ScheduledPost(models.Model):
    content = models.TextField()
    platform = models.CharField(max_length=10, choices=Platform.choices)
    attachment = models.URLField(blank=True)
    post_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Field to store additional information relevant to scheduling (optional)
    scheduling_details = models.JSONField(blank=True, null=True)

    # Field to store the actual post ID retrieved from the platform (optional)
    post_id = models.CharField(max_length=255, blank=True, null=True)

    # Field to store platform-specific analytics data (optional)
    analytics_data = models.JSONField(blank=True, null=True)


#class AnalyticsData(models.Model):
    # This model remains the same for storing general analytics data

    # ... (definition of fields for specific analytics data)
    # Fo