# Generated by Django 5.1.4 on 2025-01-20 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='products/')),
            ],
        ),
        migrations.CreateModel(
            name='SourcingProductRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('link', models.URLField(max_length=500)),
                ('image', models.ImageField(upload_to='sourcing_products/')),
                ('description', models.TextField()),
                ('added_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_by', models.CharField(blank=True, max_length=255, null=True)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('review', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('category', models.CharField(default='', max_length=255)),
                ('description', models.TextField()),
                ('inventory', models.PositiveIntegerField(default=0)),
                ('created_by', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('vendor', models.CharField(default='', max_length=255)),
                ('images', models.ManyToManyField(related_name='products', to='staff_panel.productimage')),
            ],
        ),
    ]
