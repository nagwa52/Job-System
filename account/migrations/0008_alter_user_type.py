# Generated by Django 4.0.5 on 2022-06-14 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_user_date_of_birth_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('admin', 'Admin'), ('recruiter', 'Recruiter'), ('developer', 'Developer')], max_length=10, verbose_name='User Type'),
        ),
    ]