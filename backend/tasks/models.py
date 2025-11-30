from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField(null=True, blank=True)
    estimated_hours = models.FloatField(default=1)
    importance = models.IntegerField(default=5)
    dependencies = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='blocked_by')

    def __str__(self):
        return self.title
