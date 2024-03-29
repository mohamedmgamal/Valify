# Generated by Django 3.1.7 on 2022-01-22 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0003_customuser_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(error_messages={'unique': 'This email is already registered'}, max_length=255, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
