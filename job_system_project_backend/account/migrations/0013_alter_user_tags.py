# Generated by Django 4.0.5 on 2022-06-16 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tag', '0001_initial'),
        ('account', '0012_alter_user_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='tag.tag'),
        ),
    ]