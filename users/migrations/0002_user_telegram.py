# Generated by Django 5.1.3 on 2024-11-13 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='telegram',
            field=models.CharField(default=1, max_length=200, verbose_name='Telegram'),
            preserve_default=False,
        ),
    ]
