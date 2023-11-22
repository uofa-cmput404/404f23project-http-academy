

from django.db import models

from authors.models import AppUser


class Like(models.Model):
    type = models.CharField(max_length=5, default="Like", editable=False)
    author = models.ForeignKey(AppUser, related_name="liked", on_delete=models.CASCADE)
    object = models.URLField(max_length=500, editable=False)
    summary = models.CharField(max_length=500)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author','object'], name="unique_like")
        ]
    
