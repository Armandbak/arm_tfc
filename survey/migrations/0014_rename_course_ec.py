# Generated by Django 5.0.6 on 2024-06-08 12:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0013_uenseignement_alter_course_teacher_and_more'),
        ('teacher', '0003_remove_teacher_salary_teacher_profile_pic'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Course',
            new_name='Ec',
        ),
    ]
