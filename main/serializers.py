from .models import Theme, Note, Profile
from rest_framework import serializers


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['pk', 'title', 'text', 'theme', 'author', 'importance', 'created', 'is_active']
