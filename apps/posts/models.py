from django.db import models
from model_utils.managers import QueryManager
from apps.shared.models import ModelDefault
from apps.users.models import CustomUser


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class Post(ModelDefault):

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='blog_posts')
    text = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    objects = QueryManager(canceled_at__isnull=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-id",]
