# Generated by Django 3.1.2 on 2020-11-29 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_name', models.CharField(max_length=255)),
                ('pet_bday', models.DateField()),
                ('pet_bodycond', models.IntegerField()),
                ('pet_weight', models.IntegerField()),
                ('pet_act_lvl', models.CharField(max_length=48)),
                ('pet_gender', models.CharField(max_length=10)),
                ('pet_goal', models.IntegerField()),
                ('pet_intact', models.CharField(max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=255)),
                ('birthday', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User_diary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calories', models.IntegerField()),
                ('fat', models.IntegerField()),
                ('carbs', models.IntegerField()),
                ('protein', models.IntegerField()),
                ('activity', models.CharField(max_length=48)),
                ('calories_burned', models.IntegerField()),
                ('food_item', models.CharField(max_length=48)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='users_diaries', to='App_PackTrack.user')),
            ],
        ),
        migrations.CreateModel(
            name='Pet_diary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pet_cals', models.IntegerField()),
                ('pet_fat', models.IntegerField()),
                ('pet_carbs', models.IntegerField()),
                ('pet_protein', models.IntegerField()),
                ('pet_activity', models.CharField(max_length=48)),
                ('pet_calburned', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pets_diaries', to='App_PackTrack.pet')),
            ],
        ),
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_weight', models.IntegerField()),
                ('height', models.IntegerField()),
                ('gender', models.CharField(max_length=2)),
                ('activity_lvl', models.CharField(max_length=48)),
                ('goal', models.IntegerField()),
                ('carb_percent', models.IntegerField()),
                ('fat_percent', models.IntegerField()),
                ('protein_percent', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bodies', to='App_PackTrack.user')),
            ],
        ),
    ]
