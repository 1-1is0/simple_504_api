# Generated by Django 5.0.2 on 2024-02-28 22:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lesson", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=128, verbose_name="course name")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="created at"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="updated at"),
                ),
            ],
            options={
                "verbose_name": "CourseModel",
                "verbose_name_plural": "CourseModels",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddField(
            model_name="unitmodel",
            name="audio",
            field=models.FileField(
                blank=True, upload_to="unit_audios/", verbose_name="audio"
            ),
        ),
        migrations.AddField(
            model_name="unitmodel",
            name="description",
            field=models.TextField(blank=True, verbose_name="description"),
        ),
        migrations.AlterField(
            model_name="unitmodel",
            name="lesson",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="lesson.coursemodel",
                verbose_name="Course",
            ),
        ),
        migrations.DeleteModel(
            name="LessonModel",
        ),
    ]
