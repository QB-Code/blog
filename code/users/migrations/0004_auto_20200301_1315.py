# Generated by Django 2.2.10 on 2020-03-01 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20200301_1258'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentRate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.MyUser')),
            ],
        ),
        migrations.RemoveField(
            model_name='comment',
            name='rated_users',
        ),
        migrations.AddField(
          model_name='comment',
          name='rated_users',
          field=models.ManyToManyField(related_name='rated_comments', through='users.CommentRate', to='users.MyUser'),
        ),
        migrations.AddField(
            model_name='commentrate',
            name='comments',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Comment'),
        ),
    ]
