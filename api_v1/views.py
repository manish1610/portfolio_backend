from api_v1.models import Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework import serializers
from django.conf import settings


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


class GithubProjects(APIView):
    def get(self, request, format=None):
        github_username = settings.GITHUB_USERNAME
        github_token = settings.GITHUB_TOKEN


        url = f"https://api.github.com/users/{github_username}/repos"
        headers = {"Authorization": f"token {github_token}"}
        response = requests.get(url, headers=headers)
        n_latest = request.query_params.get('n_latest', None)

        if not response.status_code == status.HTTP_200_OK:
            return Response({"error": "Failed to fetch data from GitHub"}, status=response.status_code)

        github_repos = response.json()
        projects = [
            {
                field: repo[field]
                for field in ['name', 'created_at', 'updated_at', 'url', 'description', 'html_url']
            }
            for repo in github_repos
        ]

        sorted_projects = sorted(projects, key=lambda project: project['updated_at'], reverse=True)
        if n_latest:
            sorted_projects = sorted_projects[:int(n_latest)]

        return Response(sorted_projects, status.HTTP_200_OK)
