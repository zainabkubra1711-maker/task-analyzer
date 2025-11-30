from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils.dateparse import parse_date

from .models import Task
from .serializers import TaskSerializer
from .scoring import score_task


def build_explanation(task, score, strategy):
    parts = []
    parts.append(f"Strategy: {strategy}.")
    if task.due_date:
        parts.append(f"Due date: {task.due_date}.")
    parts.append(f"Importance: {task.importance}.")
    parts.append(f"Estimated hours: {task.estimated_hours}.")
    dependents = task.blocked_by.count()
    if dependents > 0:
        parts.append(f"Blocks {dependents} other task(s).")
    parts.append(f"Final score: {score:.2f}.")
    return " ".join(parts)


@api_view(['POST'])
def analyze_tasks(request):
    strategy = request.query_params.get('strategy', 'smart_balance')
    tasks_data = request.data

    # Expect a JSON array
    if not isinstance(tasks_data, list):
        return Response(
            {"error": "Send a JSON array of tasks"},
            status=status.HTTP_400_BAD_REQUEST
        )

    created_tasks = []
    for item in tasks_data:
        title = item.get('title')
        if not title:
            return Response(
                {"error": "Task missing title"},
                status=status.HTTP_400_BAD_REQUEST
            )

        due_str = item.get('due_date')
        due_date = parse_date(due_str) if due_str else None

        estimated_hours = item.get('estimated_hours', 1)
        importance = item.get('importance', 5)

        task = Task(
            title=title,
            due_date=due_date,
            estimated_hours=estimated_hours,
            importance=importance,
        )
        task.save()
        created_tasks.append(task)

    # Compute scores + explanations (not stored in DB, only on instances)
    tasks_with_scores = []
    for t in created_tasks:
        s = score_task(t, strategy=strategy)
        t.score = s
        t.explanation = build_explanation(t, s, strategy)
        tasks_with_scores.append(t)

    serializer = TaskSerializer(tasks_with_scores, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def suggest_tasks(request):
    strategy = request.query_params.get('strategy', 'smart_balance')
    tasks = Task.objects.all()

    tasks_scored = []
    for t in tasks:
        s = score_task(t, strategy=strategy)
        t.score = s
        t.explanation = build_explanation(t, s, strategy)
        tasks_scored.append(t)

    # Sort by score descending and take top 3
    tasks_scored.sort(key=lambda x: x.score, reverse=True)
    top_three = tasks_scored[:3]

    serializer = TaskSerializer(top_three, many=True)
    return Response(serializer.data)