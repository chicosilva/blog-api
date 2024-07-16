import datetime

from django.db import models


class CustomManager(models.Manager):
    def get_queryset(self):
        return super(CustomManager, self).\
            get_queryset().filter(canceled_at__isnull=True)


class EntriesCanceledManager(models.Manager):
    def get_queryset(self):
        return super(EntriesCanceledManager, self).\
            get_queryset().filter(canceled_at__isnull=False)


class ModelDefault(models.Model):
    class Meta:
        abstract = True
        ordering = ["-created_at"]

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    canceled_at = models.DateTimeField(editable=False, null=True, blank=True)
    update_at = models.DateTimeField(editable=False, auto_now=True)
    canceled_name = models.CharField(max_length=255, null=True, blank=True, editable=False,)
    objects = CustomManager()
    entries_canceled = EntriesCanceledManager()

    def set_canceled(self):
        self.canceled_at = datetime.datetime.now()
        return self
