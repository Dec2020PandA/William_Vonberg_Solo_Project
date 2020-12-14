# Generated by Django 3.1.2 on 2020-12-14 05:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_PackTrack', '0020_pet_diary_owner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='poster',
        ),
        migrations.AlterField(
            model_name='pet_diary',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pet_owners', to='App_PackTrack.user'),
        ),
    ]
