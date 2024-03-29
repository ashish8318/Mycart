# Generated by Django 3.0.3 on 2020-03-11 07:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20200308_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Size',
            field=models.CharField(choices=[('none', 'none'), ('S size', 'S size'), ('M size', 'M size'), ('L size', 'L size')], default='none', max_length=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='color',
            field=models.CharField(choices=[('none', 'none'), ('Red', 'Red'), ('Blue', 'Blue'), ('Green', 'Green'), ('Orange', 'Orange'), ('Yellow', 'Yellow'), ('Pink', 'Pink'), ('Purple', 'Purple'), ('Violet', 'Violet'), ('Gold', 'Gold'), ('Coral', 'Coral'), ('Brown', 'Brown'), ('White', 'white'), ('Black', 'Black'), ('Silver', 'Silver')], default='none', max_length=15),
        ),
        migrations.CreateModel(
            name='address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('countery', models.CharField(default='', max_length=30)),
                ('state', models.CharField(default='', max_length=30)),
                ('district', models.CharField(default='', max_length=30)),
                ('post', models.CharField(default='', max_length=30)),
                ('village', models.CharField(default='', max_length=30)),
                ('Home_No', models.CharField(default='', max_length=50)),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.user')),
            ],
        ),
    ]
