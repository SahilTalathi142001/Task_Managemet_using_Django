# Generated by Django 5.0.4 on 2024-05-02 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='created_by',
        ),
        migrations.AlterField(
            model_name='task',
            name='assigned_to',
            field=models.CharField(max_length=100),
        ),
    ]