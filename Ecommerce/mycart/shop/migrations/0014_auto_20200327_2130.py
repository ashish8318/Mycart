# Generated by Django 3.0.3 on 2020-03-27 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20200314_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='userorder',
            name='order_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='desc',
            field=models.TextField(help_text='Please Enter is format color : Red , ......just like  ', max_length=300),
        ),
    ]
