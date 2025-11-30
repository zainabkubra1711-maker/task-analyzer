from datetime import date

def days_until_due(due_date):
    if not due_date:
        return None
    return (due_date - date.today()).days

def score_task(task, strategy="smart_balance"):
    d = days_until_due(task.due_date)
    if d is None:
        urgency = 0
    elif d < 0:
        urgency = 20
    elif d == 0:
        urgency = 15
    elif d <= 3:
        urgency = 10
    elif d <= 7:
        urgency = 5
    else:
        urgency = 1

    importance = task.importance or 0
    effort = task.estimated_hours or 1
    dependents_count = task.blocked_by.count() if hasattr(task, "blocked_by") else 0
    dependency_score = dependents_count * 2

    if strategy == "fastest":
        effort_score = 10 / (effort + 1)
        return effort_score
    if strategy == "high_impact":
        return importance * 3 + urgency
    if strategy == "deadline":
        return urgency * 3 + importance
    if strategy == "smart_balance":
        effort_score = 5 / (effort + 1)
        return urgency * 2 + importance * 2 + effort_score + dependency_score

    return urgency + importance
