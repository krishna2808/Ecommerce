# Generated by Django 2.2 on 2022-11-21 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_auto_20221120_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='pic',
            field=models.ImageField(upload_to='images/user/2022-11-21 09:38:39.527873/'),
        ),
    ]
