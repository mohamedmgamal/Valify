# Generated by Django 3.1.7 on 2022-01-23 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Auth', '0008_otp_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='poll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('expiry_date', models.DateField()),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.AlterModelOptions(
            name='otp',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterField(
            model_name='otp',
            name='otp',
            field=models.CharField(default='936410', editable=False, max_length=6, unique=True),
        ),
        migrations.CreateModel(
            name='Choices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='poll', to='Auth.poll')),
            ],
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.choices')),
                ('poll', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Auth.poll')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'poll')},
            },
        ),
    ]
