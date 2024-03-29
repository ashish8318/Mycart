# Generated by Django 3.0.3 on 2020-03-11 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20200311_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='userid',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.user'),
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(default=0)),
                ('product_id', models.IntegerField(default=0)),
                ('product_name', models.CharField(default='', max_length=30)),
                ('order_date', models.DateField(auto_now=True)),
                ('Track', models.CharField(default='', max_length=30)),
                ('price', models.IntegerField(default=0)),
                ('product_rate', models.IntegerField(default=0)),
                ('delevered_date', models.DateField()),
                ('user_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.user')),
            ],
        ),
    ]
