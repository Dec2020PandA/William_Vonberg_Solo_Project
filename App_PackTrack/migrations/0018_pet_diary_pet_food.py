# Generated by Django 3.1.2 on 2020-12-12 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_PackTrack', '0017_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet_diary',
            name='pet_food',
            field=models.CharField(default='Dog Kibble', max_length=255),
            preserve_default=False,
        ),
    ]
