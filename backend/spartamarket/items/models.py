from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=50)


class Item(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="items", default=None,
                             null=True)

    category = models.ForeignKey(Category, related_name="items", on_delete=models.CASCADE, default=None, null=True)

    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_items"
    )

    def __str__(self):
        return self.title