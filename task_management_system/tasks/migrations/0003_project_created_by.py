# Generated by Django 5.0.4 on 2024-05-02 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_remove_project_created_by_alter_task_assigned_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='created_by',
            field=models.CharField(default='Sahil', max_length=100),
        ),
    ]
