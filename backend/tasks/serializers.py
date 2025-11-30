from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    score = serializers.FloatField(read_only=True)
    explanation = serializers.CharField(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'title', 'due_date', 'estimated_hours', 'importance', 'dependencies', 'score', 'explanation']
