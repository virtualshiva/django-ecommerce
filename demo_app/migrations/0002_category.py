# Generated by Django 4.0.6 on 2022-07-18 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]