# Generated by Django 3.2.8 on 2021-10-16 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_merge_0019_auto_20211016_1443_0021_auto_20211016_1243'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='document',
            options={'ordering': ['-uploaded_at']},
        ),
    ]
