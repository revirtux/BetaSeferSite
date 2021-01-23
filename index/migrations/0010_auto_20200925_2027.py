# Generated by Django 3.0.1 on 2020-09-25 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0009_auto_20200925_1627'),
    ]

    operations = [
        migrations.RenameField(
            model_name='house',
            old_name='moto',
            new_name='motto',
        ),
        migrations.AddField(
            model_name='house',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='banners'),
        ),
        migrations.AlterField(
            model_name='user',
            name='state',
            field=models.CharField(choices=[('G', 'player'), ('P', 'pensioner'), ('Z', 'zombie'), ('C', 'commemoration'), ('T', 'testing')], default='G', max_length=1),
        ),
    ]
