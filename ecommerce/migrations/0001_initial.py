# Generated by Django 3.1.7 on 2021-03-01 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MainBuyer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('email', models.EmailField(blank=True, max_length=64, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('photo', models.FileField(blank=True, null=True, upload_to='photo', verbose_name='product_photo')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.brand')),
            ],
        ),
        migrations.AddField(
            model_name='brand',
            name='mainbuyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.mainbuyer'),
        ),
    ]
