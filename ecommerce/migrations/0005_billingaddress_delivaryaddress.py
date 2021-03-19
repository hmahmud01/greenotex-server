# Generated by Django 3.1.7 on 2021-03-16 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_auto_20210313_1036'),
    ]

    operations = [
        migrations.CreateModel(
            name='DelivaryAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=128, null=True)),
                ('city', models.CharField(blank=True, max_length=128, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=128, null=True)),
                ('country', models.CharField(blank=True, max_length=128, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.localbuyer')),
            ],
        ),
        migrations.CreateModel(
            name='BillingAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=128, null=True)),
                ('city', models.CharField(blank=True, max_length=128, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=128, null=True)),
                ('country', models.CharField(blank=True, max_length=128, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.localbuyer')),
            ],
        ),
    ]
