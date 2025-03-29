# Generated by Django 5.1.7 on 2025-03-29 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boreka', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='is_completed',
        ),
        migrations.AddField(
            model_name='task',
            name='priority_level',
            field=models.CharField(choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium', max_length=10),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Completed', 'Completed')], default='Pending', max_length=10),
        ),
    ]
