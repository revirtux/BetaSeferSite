# Generated by Django 3.1.1 on 2021-01-23 21:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0020_auto_20200928_2326'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameRank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('badge', models.ImageField(blank=True, null=True, upload_to='game_badges')),
                ('min_place', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('getting_points_desc', models.CharField(max_length=2048)),
                ('leveling_desc', models.CharField(max_length=2048)),
                ('category', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='index.category')),
                ('managers', models.ManyToManyField(to='index.User')),
                ('ranks', models.ManyToManyField(to='index.GameRank')),
            ],
        ),
    ]
