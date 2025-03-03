# Generated by Django 5.1.5 on 2025-03-01 10:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_alter_task_labels'),
        ('users', '0004_delete_user_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='Task',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_tasks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='Task',
            name='executor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsible_tasks', to=settings.AUTH_USER_MODEL),
        ),
    ]
