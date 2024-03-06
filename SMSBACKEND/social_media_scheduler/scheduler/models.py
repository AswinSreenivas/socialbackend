from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import URLValidator
from django.utils.text import slugify

class User(AbstractUser):
    # Add additional user fields as needed
    # Examples:
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True) 

class SocialProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Separate fields for storing access tokens for each platform
    facebook_access_token = models.CharField(max_length=255, null=True, blank=True)
    instagram_access_token = models.CharField(max_length=255, null=True, blank=True)

    # Field to store the user's profile picture URL
    profile_picture_url = models.URLField(max_length=255, null=True, blank=True)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Fields for scheduled publishing and social media post ID
    scheduled_at = models.DateTimeField(null=True, blank=True)
    social_media_post_id = models.CharField(max_length=255, null=True, blank=True)

    # Slug field for generating unique URLs for posts (optional)
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.content[:50]}-{self.id}")  # Generate slug based on content and ID
        super().save(*args, **kwargs)  # Call the original save method

class PostImage(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')  # Adjust upload path as needed

class PostLink(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    url = models.URLField(validators=[URLValidator])  # Validate URL format
