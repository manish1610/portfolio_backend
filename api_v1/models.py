from django.db import models


class Comment(models.Model):
    added_by = models.CharField(max_length=100)
    description = models.TextField(help_text="Actual content of the comment")
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
