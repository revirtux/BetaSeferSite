# Generated by Django 3.0.1 on 2020-03-06 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_auto_20200229_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='multipoint',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='note',
            field=models.CharField(blank=True, default='', max_length=256),
        ),
    ]
