# tasks/models.py

from django.db import models



class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_by = models.CharField(max_length=100, default='Sahil')  # Add the created_by field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    project = models.ForeignKey(Project, related_name='tasks', on_delete=models.CASCADE)
    assigned_to = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

