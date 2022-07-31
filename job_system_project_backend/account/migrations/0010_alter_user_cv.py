# Generated by Django 4.0.5 on 2022-06-14 19:14

import account.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='cv',
            field=models.FileField(blank=True, null=True, upload_to='media', validators=[account.validator.validate_file_extension], verbose_name='CV'),
        ),
    ]