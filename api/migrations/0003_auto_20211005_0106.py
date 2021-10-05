# Generated by Django 3.2.7 on 2021-10-05 01:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_lesson_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='emergency_contact_name',
            field=models.CharField(default='admin emergency contact', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='emergency_contact_phone',
            field=models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')]),
        ),
        migrations.AddField(
            model_name='user',
            name='is_instructor',
            field=models.BooleanField(default=False),
        ),
    ]