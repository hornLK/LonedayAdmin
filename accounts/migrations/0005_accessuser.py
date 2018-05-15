# Generated by Django 2.0.4 on 2018-05-18 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20180429_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, db_index=True, max_length=64, unique=True)),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True)),
                ('accessuser_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'access用户表',
                'verbose_name_plural': 'access用户表',
            },
        ),
    ]
