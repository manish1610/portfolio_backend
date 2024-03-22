from api_v1.models import Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'added_by', 'description']


class AddComment(APIView):
    def post(self, request, format=None):
        print("before")
        serializer = CommentSerializer(data=request.data)
        print("here")
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LatestGithubProjects(APIView):
    def get(self, request, format=None):
        github_username = "your_github_username"
        github_token = "your_github_token"

        url = f"https://api.github.com/users/{github_username}/repos"
        headers = {"Authorization": f"token {github_token}"}
        response = requests.get(url, headers=headers)

        if not response.status_code == status.HTTP_200_OK:
            return Response({"error": "Failed to fetch data from GitHub"}, status=response.status_code)

        github_repos = response.json()
        projects = [
            {"name": repo["name"], "created_at": repo["created_at"]}
            for repo in github_repos
        ]

        return Response(projects, status.HTTP_200_OK)
