# Generated by Django 5.1.2 on 2024-10-16 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_game_options_game_target_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='target_number',
            field=models.IntegerField(default=0),
        ),
    ]
