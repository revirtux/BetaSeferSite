# Generated by Django 3.0.1 on 2020-09-25 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0013_house_text_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='house',
            name='headers_color',
            field=models.CharField(default='', max_length=8),
        ),
    ]
