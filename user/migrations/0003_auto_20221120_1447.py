# Generated by Django 2.2 on 2022-11-20 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20221120_1447'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pic',
            field=models.ImageField(upload_to='images/user/2022-11-20 14:47:13.417056/'),
        ),
    ]
