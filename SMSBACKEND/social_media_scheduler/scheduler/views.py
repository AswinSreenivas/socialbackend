from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .models import User, Post, SocialProfile
from .serializers import UserSerializer, PostSerializer, PostAnalyticsSerializer
from .forms import UserLoginForm, UserRegistrationForm, PostForm
from requests.auth import HTTPBasicAuth
import requests

# ... (Replace with your social provider libraries, e.g., django-allauth-microsoft)

def publish_post(post, access_token):
    # Replace with the appropriate Graph API endpoint URL for posting
    url = f"https://graph.microsoft.com/v1.0/me/feed"
    data = {
        "message": post.content,
        # ... (add other relevant fields for the post)
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    auth = HTTPBasicAuth("clientId", "clientSecret")  # Replace with your Microsoft Graph credentials
    response = requests.post(url, headers=headers, json=data, auth=auth)
    if response.status_code == 201:
        # Handle successful post creation (e.g., update post status)
        return True
    else:
        # Handle errors (e.g., log error, retry mechanism)
        return False

def retrieve_analytics(post_id, access_token):
    # Replace with the appropriate Graph API endpoint URL for analytics
    url = f"https://graph.microsoft.com/v1.0/{post_id}/insights/metrics"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    auth = HTTPBasicAuth("clientId", "clientSecret")  # Replace with your Microsoft Graph credentials
    response = requests.get(url, headers=headers, auth=auth)
    if response.status_code == 200:
        # Parse the response (JSON) to access analytics data
        analytics_data = response.json()
        return analytics_data
    else:
        # Handle errors or no data available
        return None


class UserRegistrationView(APIView):
    def post(self, request):
        # ... (handle user registration logic using a serializer)
        return Response(serialized_user_data, status=status.HTTP_201_CREATED)


class PostListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        posts = user.post_set.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user=request.user)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(user=request.user)
            access_token = request.user.socialprofile.microsoft_access_token  # Replace with appropriate field for your platform
            if publish_post(post, access_token):
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Failed to publish post"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk, user=request.user)
        access_token = request.user.socialprofile.microsoft_access_token  # Replace with appropriate field for your platform
        analytics_data = retrieve_analytics(post.id, access_token)
        if analytics_data:
            return
