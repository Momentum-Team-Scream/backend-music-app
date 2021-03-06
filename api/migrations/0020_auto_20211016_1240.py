# Generated by Django 3.2.8 on 2021-10-16 16:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0019_auto_20211015_1721"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="students",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                related_name="document_students",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="document",
            name="tags",
            field=models.ManyToManyField(
                blank=True, null=True, related_name="document_tags", to="api.Tag"
            ),
        ),
        migrations.AlterField(
            model_name="tag",
            name="tag",
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
