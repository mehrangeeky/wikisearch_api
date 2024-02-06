from django.db import models
from django.contrib.auth.models import User


class WikiSearchLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    article = models.CharField(max_length=255)
    word_count = models.IntegerField(default=0)
    word_frequency = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "WikiSearchLog"
        verbose_name_plural = "WikiSearchLogs"
        ordering = ["-created_at"]

    def __str__(self):
        """String representation of WikiSearchLogs"""
        return "{} - {} - {}".format(
            self.article,
            self.word_count,
            self.created_at.date(),
        )
