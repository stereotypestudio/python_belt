# Generated by Django 2.0.6 on 2018-06-22 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0003_auto_20180621_2008'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=255)),
                ('likes', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='users_app.User')),
            ],
        ),
        migrations.RemoveField(
            model_name='comments',
            name='author',
        ),
        migrations.RemoveField(
            model_name='comments',
            name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
    ]
