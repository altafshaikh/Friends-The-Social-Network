# Generated by Django 2.1.7 on 2019-09-10 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_comment_flag'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='count',
        ),
        migrations.AddField(
            model_name='post',
            name='comment_count',
            field=models.IntegerField(default=0),
        ),
    ]