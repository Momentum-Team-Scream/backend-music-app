# Generated by Django 3.2.8 on 2021-10-12 14:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0016_document_author"),
    ]

    operations = [
        migrations.CreateModel(
            name="Tag",
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
                ("tag", models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name="document",
            name="students",
            field=models.ManyToManyField(
                blank=True,
                related_name="document_students",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="author",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="documents",
                to="api.user",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="document",
            name="tags",
            field=models.ManyToManyField(
                blank=True, related_name="document_tags", to="api.Tag"
            ),
        ),
    ]
