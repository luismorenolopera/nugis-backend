# Generated by Django 2.1.2 on 2018-10-16 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='in_youtube',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='track',
            name='thumbnail',
            field=models.URLField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='track',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]
