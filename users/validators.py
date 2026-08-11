import re
from rest_framework import serializers


def validate_youtube_url(value):
    """Проверяет, что ссылка ведёт на YouTube"""
    if not value:
        return value

    # Проверяем, что ссылка содержит youtube.com или youtu.be
    if not re.search(r'(youtube\.com|youtu\.be)', value):
        raise serializers.ValidationError("Разрешены только ссылки на YouTube")

    return value
