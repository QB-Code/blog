# Generated by Django 2.2.10 on 2020-07-10 05:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20200705_1530'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='users/comments/pictures')),
                ('comment', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='users.Comment')),
            ],
        ),
        migrations.DeleteModel(
            name='CommentPhoto',
        ),
    ]
