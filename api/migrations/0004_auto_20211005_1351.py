# Generated by Django 3.2.7 on 2021-10-05 17:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0003_auto_20211005_0106"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="lesson",
            options={"ordering": ["-lesson_date"]},
        ),
        migrations.AlterField(
            model_name="user",
            name="emergency_contact_phone",
            field=models.CharField(
                max_length=17,
                validators=[
                    django.core.validators.RegexValidator(
                        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
                        regex="^\\+?1?\\d{9,15}$",
                    )
                ],
            ),
        ),
    ]
