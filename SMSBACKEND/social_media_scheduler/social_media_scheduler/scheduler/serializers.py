from rest_framework import serializers
from .models import User, Post, SocialProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'created_at')

class PostAnalyticsSerializer(serializers.Serializer):
    # ... (Define fields specific to your retrieved post analytics data)
    # For example:
    # impressions = serializers.IntegerField()
    # clicks = serializers.IntegerField()
    # ...

#from rest_framework import serializers
#from .models import User, Post, SocialProfile

'''class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile_pic')  # Add profile_pic if applicable

    # Optional: Add a custom validation method for the profile_pic field
    def validate_profile_pic(self, value):
        # Implement validation logic for the profile picture (e.g., size, format)
        return value

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'created_at', 'scheduled_at')  # Add scheduled_at if applicable

    # Optional: Add a custom validation method for the scheduled_at field
    def validate_scheduled_at(self, value):
        # Implement validation logic for the scheduled publishing time (e.g., in the future)
        return value

class PostAnalyticsSerializer(serializers.Serializer):
    impressions = serializers.IntegerField()
    clicks = serializers.IntegerField()
    # ... (Add other relevant fields specific to your retrieved post analytics data)

    # Optional: Add a method to handle potential transformation of analytics data
    def to_representation(self, instance):
        # Implement logic to transform or format the analytics data before serialization
        # (e.g., convert to desired units, add calculations)
        return super().to_representation(instance)'''
