# Generated by Django 3.0.3 on 2020-03-14 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0012_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='user_email',
            field=models.CharField(default='', max_length=40),
        ),
    ]
