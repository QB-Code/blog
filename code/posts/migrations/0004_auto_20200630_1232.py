# Generated by Django 2.2.10 on 2020-06-30 09:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20200630_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='rubric',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.Rubric'),
        ),
    ]
