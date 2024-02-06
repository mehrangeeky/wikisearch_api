# serializers.py
from rest_framework import serializers
from search_app.models import WikiSearchLog


class WikiSearchLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = WikiSearchLog
        fields = (
            "id",
            "article",
            "word_count",
            "word_frequency",
            "created_at",
        )
