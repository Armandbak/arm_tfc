# Generated by Django 5.0.6 on 2024-05-29 08:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_remove_teacherprofile_user_delete_studentprofile_and_more'),
        ('teacher', '0002_teacher_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='date_debut',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='date_fin',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='teacher.teacher'),
            preserve_default=False,
        ),
    ]
