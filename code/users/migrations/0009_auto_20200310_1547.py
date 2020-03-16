# Generated by Django 2.2.10 on 2020-03-10 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200301_1726'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_released',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='comment',
            name='released_at',
            field=models.DateTimeField(null=True),
        ),
    ]