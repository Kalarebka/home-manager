# Generated by Django 4.0.2 on 2022-02-25 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_board_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_images'),
        ),
    ]